from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from .router_incidents import router as incidents_router
from .router_rag import router as rag_router
from .router_db import router as db_router

app = FastAPI(title="Imperial Court of the Port", version="0.1.0")

# Allow frontend origins
origins = [
    "http://localhost:3000",  # or wherever your frontend runs
    "http://127.0.0.1:3000",
	"https://imperial-court-of-the-port.vercel.app/"
]

app.add_middleware(
		CORSMiddleware,
		allow_origins=origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
)


@app.get("/health")
async def health() -> Dict[str, str]:
	return {"status": "ok", "service": "imperial-court-backend"}

@app.get("/health/ready")
async def readiness() -> Dict[str, str]:
	# Add more sophisticated readiness checks here if needed
	# For example, check database connectivity, Redis connectivity, etc.
	return {"status": "ready", "service": "imperial-court-backend"}


app.include_router(incidents_router)
app.include_router(rag_router)
app.include_router(db_router)
