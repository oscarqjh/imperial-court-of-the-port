from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

from .orchestrator import ImperialOrchestrator

router = APIRouter(prefix="/incident", tags=["incident"])


class IncidentRequest(BaseModel):
	incident_text: str


class RunResponse(BaseModel):
	run_id: str
	status: str
	result: Optional[Dict[str, Any]] = None


RUNS: Dict[str, Dict[str, Any]] = {}


@router.post("/run", response_model=RunResponse)
async def run_incident(incident_text: str = Form(...)):
	logger.info("🚨 NEW INCIDENT RECEIVED via API")
	logger.info(f"📝 Incident Text: {incident_text[:100]}{'...' if len(incident_text) > 100 else ''}")
	
	try:
		orchestrator = ImperialOrchestrator()
		logger.info("🏛️ Orchestrator initialized, beginning incident processing...")
		
		result = orchestrator.run(incident={"incident_text": incident_text})
		
		run_id = f"run_{len(RUNS) + 1}"
		RUNS[run_id] = {"status": "completed", "result": result}
		
		logger.info(f"✅ INCIDENT PROCESSING COMPLETED - Run ID: {run_id}")
		if "incident_analysis" in result:
			analysis = result["incident_analysis"]
			logger.info(f"📊 Final Classification: {analysis.get('incident_type', 'N/A')} - {analysis.get('severity', 'N/A')} severity")
		
		return RunResponse(run_id=run_id, status="completed", result=result)
		
	except Exception as e:
		logger.error(f"❌ INCIDENT PROCESSING FAILED: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Incident processing failed: {str(e)}")


@router.get("/run/{run_id}", response_model=RunResponse)
async def get_run(run_id: str):
	logger.info(f"📋 Run status requested for: {run_id}")
	
	if run_id not in RUNS:
		logger.warning(f"❓ Run not found: {run_id}")
		raise HTTPException(status_code=404, detail="run not found")
	
	entry = RUNS[run_id]
	logger.info(f"✅ Run found: {run_id} - Status: {entry['status']}")
	
	return RunResponse(run_id=run_id, status=entry["status"], result=entry.get("result"))
