from fastapi import FastAPI
from typing import Dict

from .router_incidents import router as incidents_router
from .router_rag import router as rag_router

app = FastAPI(title="Imperial Court of the Port", version="0.1.0")


@app.get("/health")
async def health() -> Dict[str, str]:
	return {"status": "ok"}


app.include_router(incidents_router)
app.include_router(rag_router)
