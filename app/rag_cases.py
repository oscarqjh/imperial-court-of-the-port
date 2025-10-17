from __future__ import annotations

from typing import List, Dict, Any
import uuid

from loguru import logger
from openpyxl import load_workbook  # type: ignore
import pandas as pd  # type: ignore

from .rag_chunking import smart_chunk
from .rag_embeddings import embed_texts
from .rag_qdrant import QdrantStore


def _row_to_text(headers: List[str], row_vals: List[Any]) -> str:
	pairs = []
	for h, v in zip(headers, row_vals):
		if v is None or (isinstance(v, float) and pd.isna(v)):
			continue
		pairs.append(f"{h}: {v}")
	return "\n".join(pairs)


def parse_excel_to_documents(path: str, sheet_name: str | None = None) -> List[Dict[str, Any]]:
	wb = load_workbook(filename=path, read_only=True, data_only=True)
	ws = wb[sheet_name] if sheet_name else wb.active
	rows = list(ws.rows)
	if not rows:
		return []
	headers = [str(c.value).strip() if c.value is not None else f"col_{i}" for i, c in enumerate(rows[0])]
	docs: List[Dict[str, Any]] = []
	for idx, r in enumerate(rows[1:], start=1):
		vals = [c.value for c in r]
		text = _row_to_text(headers, vals).strip()
		if not text:
			continue
		docs.append({
			"id": f"case_row_{idx}",
			"text": text,
			"meta": {"row_index": idx, "sheet": ws.title},
		})
	return docs


def parse_csv_to_documents(path: str) -> List[Dict[str, Any]]:
	# Try reading CSV with common encodings. Some CSVs (especially from Windows)
	# may contain characters not valid in UTF-8 (e.g. CP1252 bytes like 0x97).
	# Try utf-8 first, then fall back to cp1252 and latin-1. If all fail,
	# read bytes and decode with replacement to avoid crashing the ingest.
	df = None
	for enc in ("utf-8", "cp1252", "latin-1"):  # utf-8 first, then common fallbacks
		try:
			df = pd.read_csv(path, encoding=enc)
			if df is not None:
				logger.info(f"Read CSV {path} using encoding={enc}")
				break
		except UnicodeDecodeError as e:
			logger.warning(f"Failed to read {path} with encoding {enc}: {e}")
		except Exception as e:
			# pandas can raise other parsing/parsing-related errors; log and try next encoding
			logger.debug(f"Unexpected error reading {path} with encoding {enc}: {e}")
			continue
	if df is None:
		# Last-resort strategy: read raw bytes and decode replacing invalid bytes
		logger.warning(f"Falling back to tolerant read for CSV {path} (replacing invalid bytes)")
		import io
		with open(path, "rb") as f:
			raw = f.read()
		# try to decode as utf-8 replacing invalid sequences
		text = raw.decode("utf-8", errors="replace")
		df = pd.read_csv(io.StringIO(text))
	if df.empty:
		return []
	headers = list(df.columns.astype(str))
	docs: List[Dict[str, Any]] = []
	for idx, row in df.iterrows():
		vals = [row.get(h) for h in headers]
		text = _row_to_text(headers, vals).strip()
		if not text:
			continue
		docs.append({
			"id": f"case_row_{idx+1}",
			"text": text,
			"meta": {"row_index": int(idx+1), "sheet": "csv"},
		})
	return docs


def _upsert_docs_to_qdrant(docs: List[Dict[str, Any]], source: str, path: str, collection: str = None) -> Dict[str, int]:
	store = QdrantStore(collection=collection) if collection else QdrantStore()
	ids: List[str] = []
	vectors: List[List[float]] = []
	payloads: List[Dict[str, Any]] = []
	for d in docs:
		chunks = smart_chunk(d["text"], max_tokens=350, overlap_tokens=50)
		# Filter out empty/whitespace-only chunks before embedding
		chunks = [ch.strip() for ch in chunks if isinstance(ch, str) and ch.strip()]
		if not chunks:
			logger.debug(f"Skipping doc {d['id']} with no non-empty chunks after chunking")
			continue
		try:
			embs = embed_texts(chunks)
		except Exception as e:
			logger.warning(f"Embedding failed for row {d['id']} (path={path}): {e}; skipping row")
			continue
		for i, ch in enumerate(chunks):
			ids.append(str(uuid.uuid4()))
			vectors.append(embs[i])
			payloads.append({
				"text": ch,
				"source": source,
				"row_id": d["id"],
				"chunk_index": i,
				"row_index": d["meta"]["row_index"],
				"sheet": d["meta"].get("sheet"),
				"path": path,
			})
	if not ids:
		logger.info("No chunks to upsert; returning empty ingest stats")
		return {"rows": len(docs), "chunks": 0, "upserted": 0}
	store.upsert(ids=ids, vectors=vectors, payloads=payloads)
	return {"rows": len(docs), "chunks": len(ids), "upserted": len(ids)}


def ingest_cases_excel(path: str = "data/Case Log.xlsx", sheet_name: str | None = None, collection: str = None) -> Dict[str, int]:
	docs = parse_excel_to_documents(path, sheet_name)
	if not docs:
		return {"rows": 0, "chunks": 0, "upserted": 0}
	return _upsert_docs_to_qdrant(docs, source="case_log_excel", path=path, collection=collection)


def ingest_cases_csv(path: str = "data/case_log.csv", collection: str = None) -> Dict[str, int]:
	docs = parse_csv_to_documents(path)
	if not docs:
		return {"rows": 0, "chunks": 0, "upserted": 0}
	return _upsert_docs_to_qdrant(docs, source="case_log_csv", path=path, collection=collection)
