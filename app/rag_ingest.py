from __future__ import annotations

from typing import List, Dict, Tuple
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


def load_plain_text(path: str) -> str:
	if not os.path.exists(path):
		raise FileNotFoundError(path)
	with open(path, "r", encoding="utf-8") as f:
		return f.read()


def _filter_non_empty(chunks: List[str]) -> Tuple[List[str], List[int]]:
	filtered: List[str] = []
	indices: List[int] = []
	for i, ch in enumerate(chunks):
		s = (ch or "").strip()
		if s:
			filtered.append(s)
			indices.append(i)
	return filtered, indices


def _ingest_text(text: str, source: str, path: str) -> Dict[str, int]:
	chunks: List[str] = smart_chunk(text, max_tokens=400, overlap_tokens=60)
	filtered, idxs = _filter_non_empty(chunks)
	if not filtered:
		raise ValueError("No non-empty chunks produced from document")
	logger.info(f"Chunked into {len(chunks)} parts, {len(filtered)} non-empty")
	vectors = embed_texts(filtered)
	store = QdrantStore()
	ids = [str(uuid.uuid4()) for _ in filtered]
	payloads: List[Dict] = []
	for out_pos, ch in enumerate(filtered):
		orig_idx = idxs[out_pos]
		payloads.append({
			"text": ch,
			"source": source,
			"chunk_index": orig_idx,
			"path": path,
		})
	store.upsert(ids=ids, vectors=vectors, payloads=payloads)
	return {"chunks": len(filtered), "upserted": len(ids)}


def ingest_docx_to_qdrant(path: str, source: str = "knowledge_base") -> Dict[str, int]:
	logger.info(f"Loading DOCX: {path}")
	text = load_docx_text(path)
	return _ingest_text(text=text, source=source, path=path)


def ingest_text_to_qdrant(path: str, source: str = "knowledge_base_parsed") -> Dict[str, int]:
	logger.info(f"Loading TEXT: {path}")
	text = load_plain_text(path)
	return _ingest_text(text=text, source=source, path=path)
