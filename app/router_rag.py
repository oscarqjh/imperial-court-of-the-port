from __future__ import annotations

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .rag_ingest import ingest_docx_to_qdrant, ingest_text_to_qdrant
from .rag_embeddings import embed_texts
from .rag_qdrant import QdrantStore
from .rag_cases import ingest_cases_excel, ingest_cases_csv

router = APIRouter(prefix="/rag", tags=["rag"])


class IngestResponse(BaseModel):
	chunks: int
	upserted: int
	rows: int | None = None


class SearchRequest(BaseModel):
	query: str
	top_k: int = 5


class SearchResult(BaseModel):
	results: List[Dict[str, Any]]


@router.post("/ingest", response_model=IngestResponse)
async def ingest_kb() -> IngestResponse:
	try:
		stats = ingest_docx_to_qdrant("data/Knowledge Base.docx", source="knowledge_base")
		return IngestResponse(**stats)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest_parsed", response_model=IngestResponse)
async def ingest_parsed_kb() -> IngestResponse:
	try:
		stats = ingest_text_to_qdrant("data/parsed_knowledge_base.txt", source="knowledge_base_parsed")
		return IngestResponse(**stats)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest_cases", response_model=IngestResponse)
async def ingest_cases() -> IngestResponse:
	try:
		stats = ingest_cases_excel("data/Case Log.xlsx")
		return IngestResponse(chunks=stats["chunks"], upserted=stats["upserted"], rows=stats["rows"])
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest_cases_csv", response_model=IngestResponse)
async def ingest_cases_csv_endpoint() -> IngestResponse:
	try:
		stats = ingest_cases_csv("data/case_log.csv")
		return IngestResponse(chunks=stats["chunks"], upserted=stats["upserted"], rows=stats["rows"])
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResult)
async def rag_search(req: SearchRequest) -> SearchResult:
	try:
		vec = embed_texts([req.query])[0]
		store = QdrantStore()
		hits = store.search(vector=vec, top_k=req.top_k)
		return SearchResult(results=hits)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
