from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from crew import PortIncidentCrew

app = FastAPI(
    title="Imperial Court of the Port",
    description="An agentic AI system to manage port incidents using CrewAI",
    version="1.0.0"
)

class IncidentRequest(BaseModel):
    description: str
    severity: Optional[str] = "medium"
    location: Optional[str] = None

class IncidentResponse(BaseModel):
    status: str
    result: str
    incident_id: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Imperial Court of the Port",
        "description": "An agentic AI system to manage port incidents",
        "endpoints": {
            "/docs": "API documentation",
            "/health": "Health check",
            "/analyze-incident": "Analyze and manage port incidents"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze-incident", response_model=IncidentResponse)
async def analyze_incident(incident: IncidentRequest):
    """
    Analyze a port incident using CrewAI agents
    
    The system uses AI agents to:
    - Assess the incident severity
    - Recommend appropriate actions
    - Coordinate response procedures
    """
    try:
        crew = PortIncidentCrew()
        result = crew.analyze_incident(
            description=incident.description,
            severity=incident.severity,
            location=incident.location
        )
        
        return IncidentResponse(
            status="success",
            result=result,
            incident_id=f"INC-{hash(incident.description) % 10000:04d}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing incident: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
