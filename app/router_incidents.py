from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from loguru import logger

from .job_manager import job_manager, JobInfo, JobStatus

router = APIRouter(prefix="/incident", tags=["incident"])


class IncidentRequest(BaseModel):
	incident_text: str


class RunResponse(BaseModel):
	run_id: str
	status: str
	created_at: datetime
	started_at: Optional[datetime] = None
	completed_at: Optional[datetime] = None
	result: Optional[Dict[str, Any]] = None
	error: Optional[str] = None
	progress: Optional[int] = None
	current_step: Optional[str] = None


class JobListResponse(BaseModel):
	jobs: List[RunResponse]


@router.post("/run", response_model=RunResponse)
async def run_incident(incident_text: str = Form(...)):
	"""Submit an incident for background processing and return a run_id."""
	logger.info("🚨 NEW INCIDENT RECEIVED via API")
	logger.info(f"📝 Incident Text: {incident_text[:100]}{'...' if len(incident_text) > 100 else ''}")
	
	try:
		# Submit job to background processing
		run_id = job_manager.submit_job(incident_text)
		job_info = job_manager.get_job_status(run_id)
		
		if not job_info:
			raise HTTPException(status_code=500, detail="Failed to create job")
		
		logger.info(f"✅ INCIDENT SUBMITTED for background processing - Run ID: {run_id}")
		
		return RunResponse(
			run_id=job_info.run_id,
			status=job_info.status.value,
			created_at=job_info.created_at,
			started_at=job_info.started_at,
			completed_at=job_info.completed_at,
			result=job_info.result,
			error=job_info.error,
			progress=job_info.progress,
			current_step=job_info.current_step
		)
		
	except Exception as e:
		logger.error(f"❌ INCIDENT SUBMISSION FAILED: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Incident submission failed: {str(e)}")


@router.get("/run/{run_id}", response_model=RunResponse)
async def get_run(run_id: str):
	"""Get the status and results of a background job."""
	logger.info(f"📋 Run status requested for: {run_id}")
	
	job_info = job_manager.get_job_status(run_id)
	if not job_info:
		logger.warning(f"❓ Run not found: {run_id}")
		raise HTTPException(status_code=404, detail="Run not found")
	
	logger.info(f"✅ Run found: {run_id} - Status: {job_info.status}")
	
	return RunResponse(
		run_id=job_info.run_id,
		status=job_info.status.value,
		created_at=job_info.created_at,
		started_at=job_info.started_at,
		completed_at=job_info.completed_at,
		result=job_info.result,
		error=job_info.error,
		progress=job_info.progress,
		current_step=job_info.current_step
	)


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(limit: int = 20):
	"""List recent jobs with their status."""
	logger.info(f"📋 Listing recent jobs (limit: {limit})")
	
	jobs = job_manager.list_jobs(limit=limit)
	job_responses = []
	
	for job_info in jobs.values():
		job_responses.append(RunResponse(
			run_id=job_info.run_id,
			status=job_info.status.value,
			created_at=job_info.created_at,
			started_at=job_info.started_at,
			completed_at=job_info.completed_at,
			result=job_info.result,
			error=job_info.error,
			progress=job_info.progress,
			current_step=job_info.current_step
		))
	
	return JobListResponse(jobs=job_responses)


@router.post("/cleanup")
async def cleanup_old_jobs(max_age_hours: int = 24):
	"""Clean up old completed/failed jobs."""
	logger.info(f"🧹 Cleaning up jobs older than {max_age_hours} hours")
	
	initial_count = len(job_manager._jobs)
	job_manager.cleanup_old_jobs(max_age_hours=max_age_hours)
	final_count = len(job_manager._jobs)
	
	cleaned_count = initial_count - final_count
	logger.info(f"🧹 Cleaned up {cleaned_count} old jobs")
	
	return {"message": f"Cleaned up {cleaned_count} old jobs", "remaining_jobs": final_count}
