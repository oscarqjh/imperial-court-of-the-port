"""
Celery tasks for Imperial Court incident processing.
"""
from typing import Dict, Any
from loguru import logger

from .celery_config import celery_app
from .orchestrator import ImperialOrchestrator


@celery_app.task(bind=True, name="app.celery_tasks.process_incident")
def process_incident(self, incident_text: str) -> Dict[str, Any]:
    """
    Process an incident using the Imperial Court orchestrator.
    
    Args:
        incident_text: The incident description text
        
    Returns:
        Dictionary containing the incident analysis results
    """
    try:
        logger.info(f"🚀 Celery task {self.request.id} started processing incident")
        logger.info(f"📝 Incident Text: {incident_text[:100]}{'...' if len(incident_text) > 100 else ''}")
        
        # Update task state to indicate processing has started
        self.update_state(
            state="PROCESSING",
            meta={
                "current_step": "Initializing Imperial Court orchestrator",
                "progress": 10
            }
        )
        
        # Create progress callback function
        def progress_callback(progress: int, step: str):
            logger.info(f"📊 Progress callback called: {progress}% - {step}")
            self.update_state(
                state="PROCESSING",
                meta={
                    "current_step": step,
                    "progress": progress
                }
            )
        
        # Initialize orchestrator
        orchestrator = ImperialOrchestrator()
        
        # Process the incident with progress callbacks
        result = orchestrator.run(incident={"incident_text": incident_text}, progress_callback=progress_callback)
        
        # Update final progress
        self.update_state(
            state="PROCESSING",
            meta={
                "current_step": "Analysis complete, finalizing results",
                "progress": 95
            }
        )
        
        logger.info(f"✅ Celery task {self.request.id} completed successfully")
        if "incident_analysis" in result:
            analysis = result["incident_analysis"]
            logger.info(f"📊 Final Classification: {analysis.get('incident_type', 'N/A')} - {analysis.get('severity', 'N/A')} severity")
        
        return {
            "status": "completed",
            "result": result,
            "task_id": self.request.id
        }
        
    except Exception as e:
        logger.error(f"❌ Celery task {self.request.id} failed: {str(e)}")
        
        # Update task state to indicate failure
        self.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "current_step": "Failed during processing"
            }
        )
        
        # Re-raise the exception so Celery marks the task as failed
        raise e
