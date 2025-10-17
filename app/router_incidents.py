from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any

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
	orchestrator = ImperialOrchestrator()
	result = orchestrator.run(incident={"incident_text": incident_text})
	run_id = f"run_{len(RUNS) + 1}"
	RUNS[run_id] = {"status": "completed", "result": result}
	return RunResponse(run_id=run_id, status="completed", result=result)


@router.get("/run/{run_id}", response_model=RunResponse)
async def get_run(run_id: str):
	if run_id not in RUNS:
		raise HTTPException(status_code=404, detail="run not found")
	entry = RUNS[run_id]
	return RunResponse(run_id=run_id, status=entry["status"], result=entry.get("result"))
