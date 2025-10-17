from __future__ import annotations

from typing import List, Dict
import os
import uuid

import docx2txt  # type: ignore
from loguru import logger

from .rag_chunking import smart_chunk
from .rag_embeddings import embed_texts
from .rag_qdrant import QdrantStore


def load_docx_text(path: str) -> str:
	if not os.path.exists(path):
		raise FileNotFoundError(path)
	return docx2txt.process(path) or ""


def ingest_docx_to_qdrant(path: str, source: str = "knowledge_base") -> Dict[str, int]:
	logger.info(f"Loading DOCX: {path}")
	text = load_docx_text(path)
	chunks: List[str] = smart_chunk(text, max_tokens=400, overlap_tokens=60)
	logger.info(f"Chunked into {len(chunks)} parts")
	vectors = embed_texts(chunks)
	store = QdrantStore()
	ids = [str(uuid.uuid4()) for _ in chunks]
	payloads: List[Dict] = []
	for idx, ch in enumerate(chunks):
		payloads.append({
			"text": ch,
			"source": source,
			"chunk_index": idx,
			"path": path,
		})
	store.upsert(ids=ids, vectors=vectors, payloads=payloads)
	return {"chunks": len(chunks), "upserted": len(ids)}
