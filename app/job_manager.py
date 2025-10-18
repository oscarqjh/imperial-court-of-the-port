"""
Background job management for Imperial Court incident processing using Celery.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
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
        # Don't store jobs in memory - use Celery task ID as run_id directly
        pass
    
    def submit_job(self, incident_text: str) -> str:
        """Submit a new job and return the task ID as run_id."""
        # Submit task to Celery
        from .celery_tasks import process_incident
        celery_task = process_incident.delay(incident_text)
        
        # Use Celery task ID as run_id to avoid reload issues
        run_id = celery_task.id
        
        logger.info(f"📋 Job submitted with run_id (task_id): {run_id}")
        return run_id
    
    def get_job_status(self, run_id: str) -> Optional[JobInfo]:
        """Get job status and results directly from Celery using task ID."""
        try:
            # Get task status from Celery using run_id as task_id
            celery_task = celery_app.AsyncResult(run_id)
            
            # Create job info based on Celery task state
            job_info = JobInfo(
                run_id=run_id,
                celery_task_id=run_id,
                status=JobStatus.QUEUED,
                created_at=datetime.now(timezone.utc)  # We can't recover the original created_at
            )
            
            if celery_task.state == "PENDING":
                job_info.status = JobStatus.QUEUED
            elif celery_task.state == "PROCESSING":
                job_info.status = JobStatus.PROCESSING
                job_info.started_at = datetime.now(timezone.utc)
                
                # Update progress info if available
                if celery_task.info and isinstance(celery_task.info, dict):
                    job_info.progress = celery_task.info.get("progress")
                    job_info.current_step = celery_task.info.get("current_step")
                    
            elif celery_task.state == "SUCCESS":
                job_info.status = JobStatus.COMPLETED
                job_info.completed_at = datetime.now(timezone.utc)
                
                # Get the result
                task_result = celery_task.result
                if isinstance(task_result, dict) and "result" in task_result:
                    job_info.result = task_result["result"]
                    
            elif celery_task.state == "FAILURE":
                job_info.status = JobStatus.FAILED
                job_info.completed_at = datetime.now(timezone.utc)
                
                # Get error information
                if celery_task.info and isinstance(celery_task.info, dict):
                    job_info.error = celery_task.info.get("error", str(celery_task.info))
                else:
                    job_info.error = str(celery_task.info) if celery_task.info else "Unknown error"
            
            return job_info
            
        except Exception as e:
            logger.error(f"Error getting job status for {run_id}: {e}")
            return None
    
    def list_jobs(self, limit: int = 50) -> Dict[str, JobInfo]:
        """List recent jobs with updated status."""
        # Note: Without persistent storage, we can't list historical jobs
        # This method would need Redis/database storage to work properly
        logger.warning("list_jobs not supported without persistent storage")
        return {}
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed/failed jobs."""
        # Note: Celery handles task cleanup automatically based on result_expires setting
        # No manual cleanup needed when using Celery task IDs directly
        logger.info("Celery handles automatic task cleanup based on result_expires setting")


# Global job manager instance
job_manager = CeleryJobManager()
