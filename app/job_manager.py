"""
Background job management for Imperial Court incident processing using Celery.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, asdict
from loguru import logger

from .celery_config import celery_app


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class JobInfo:
    run_id: str
    celery_task_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    incident_text: Optional[str] = None
    progress: Optional[int] = None
    current_step: Optional[str] = None


class CeleryJobManager:
    """Manages background jobs for incident processing using Celery."""
    
    def __init__(self):
        # In-memory job store to persist jobs across requests
        # This survives until the server restarts
        self._jobs: Dict[str, JobInfo] = {}
        self._job_order: List[str] = []  # Track submission order
    
    def submit_job(self, incident_text: str) -> str:
        """Submit a new job and return the task ID as run_id."""
        # Submit task to Celery
        from .celery_tasks import process_incident
        celery_task = process_incident.delay(incident_text)
        
        # Use Celery task ID as run_id to avoid reload issues
        run_id = celery_task.id
        
        # Store job info in memory
        job_info = JobInfo(
            run_id=run_id,
            celery_task_id=run_id,
            status=JobStatus.QUEUED,
            created_at=datetime.now(timezone.utc),
            incident_text=incident_text[:200] + "..." if len(incident_text) > 200 else incident_text
        )
        
        self._jobs[run_id] = job_info
        self._job_order.insert(0, run_id)  # Add to front (newest first)
        
        logger.info(f"📋 Job submitted and stored in memory - Run ID: {run_id}")
        logger.info(f"📊 Total jobs in memory: {len(self._jobs)}")
        
        return run_id
    
    def get_job_status(self, run_id: str) -> Optional[JobInfo]:
        """Get job status and update in-memory store with latest info from Celery."""
        try:
            # Get task status from Celery using run_id as task_id
            celery_task = celery_app.AsyncResult(run_id)
            
            logger.debug(f"🔍 Celery task state: {celery_task.state}")
            logger.debug(f"🔍 Celery task info: {celery_task.info}")
            
            # Get existing job info from memory or create new one
            job_info = self._jobs.get(run_id)
            if not job_info:
                # Job not in memory (maybe from before server restart)
                job_info = JobInfo(
                    run_id=run_id,
                    celery_task_id=run_id,
                    status=JobStatus.QUEUED,
                    created_at=datetime.now(timezone.utc)
                )
                self._jobs[run_id] = job_info
                if run_id not in self._job_order:
                    self._job_order.append(run_id)
            
            # Update status based on Celery task state
            if celery_task.state == "PENDING":
                job_info.status = JobStatus.QUEUED
            elif celery_task.state == "PROCESSING":
                job_info.status = JobStatus.PROCESSING
                if not job_info.started_at:
                    job_info.started_at = datetime.now(timezone.utc)
                
                # Update progress info if available
                if celery_task.info and isinstance(celery_task.info, dict):
                    job_info.progress = celery_task.info.get("progress")
                    job_info.current_step = celery_task.info.get("current_step")
                    
            elif celery_task.state == "SUCCESS":
                job_info.status = JobStatus.COMPLETED
                if not job_info.completed_at:
                    job_info.completed_at = datetime.now(timezone.utc)
                
                # Set progress to 100% for completed jobs
                job_info.progress = 100
                job_info.current_step = "Completed"
                
                # Get the result
                task_result = celery_task.result
                if isinstance(task_result, dict) and "result" in task_result:
                    job_info.result = task_result["result"]
                    
            elif celery_task.state == "FAILURE":
                job_info.status = JobStatus.FAILED
                if not job_info.completed_at:
                    job_info.completed_at = datetime.now(timezone.utc)
                
                # Keep the last progress value and update step to indicate failure
                job_info.current_step = "Failed"
                
                # Get error information
                if celery_task.info and isinstance(celery_task.info, dict):
                    job_info.error = celery_task.info.get("error", str(celery_task.info))
                else:
                    job_info.error = str(celery_task.info) if celery_task.info else "Unknown error"
            
            # Update the job in memory
            self._jobs[run_id] = job_info
            
            return job_info
            
        except Exception as e:
            logger.error(f"Error getting job status for {run_id}: {e}")
            # Return existing job info if available, even if Celery query failed
            return self._jobs.get(run_id)
    
    def list_jobs(self, limit: int = 50) -> Dict[str, JobInfo]:
        """List jobs from memory and update their status by polling Celery."""
        logger.info(f"📋 Listing jobs from memory (limit: {limit})")
        
        # Update status of all jobs by polling Celery (but don't overwrite memory on errors)
        updated_jobs = {}
        for run_id in self._job_order[:limit]:  # Respect limit
            if run_id in self._jobs:
                # Get fresh status from Celery (this updates memory)
                fresh_job_info = self.get_job_status(run_id)
                if fresh_job_info:
                    updated_jobs[run_id] = fresh_job_info
                else:
                    # If Celery query failed, use what we have in memory
                    updated_jobs[run_id] = self._jobs[run_id]
        
        logger.info(f"📊 Returning {len(updated_jobs)} jobs (total in memory: {len(self._jobs)})")
        
        return updated_jobs
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed/failed jobs."""
        # Note: Celery handles task cleanup automatically based on result_expires setting
        # No manual cleanup needed when using Celery task IDs directly
        logger.info("Celery handles automatic task cleanup based on result_expires setting")


# Global job manager instance
job_manager = CeleryJobManager()
