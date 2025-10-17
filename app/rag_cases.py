from __future__ import annotations

from typing import List, Dict, Any

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
	df = pd.read_csv(path)
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


def _upsert_docs_to_qdrant(docs: List[Dict[str, Any]], source: str, path: str) -> Dict[str, int]:
	store = QdrantStore()
	ids: List[str] = []
	vectors: List[List[float]] = []
	payloads: List[Dict[str, Any]] = []
	for d in docs:
		chunks = smart_chunk(d["text"], max_tokens=350, overlap_tokens=50)
		embs = embed_texts(chunks)
		for i, ch in enumerate(chunks):
			ids.append(f"{d['id']}_ch{i}")
			vectors.append(embs[i])
			payloads.append({
				"text": ch,
				"source": source,
				"row_id": d["id"],
				"row_index": d["meta"]["row_index"],
				"sheet": d["meta"].get("sheet"),
				"path": path,
			})
	store.upsert(ids=ids, vectors=vectors, payloads=payloads)
	return {"rows": len(docs), "chunks": len(ids), "upserted": len(ids)}


def ingest_cases_excel(path: str = "data/Case Log.xlsx", sheet_name: str | None = None) -> Dict[str, int]:
	docs = parse_excel_to_documents(path, sheet_name)
	if not docs:
		return {"rows": 0, "chunks": 0, "upserted": 0}
	return _upsert_docs_to_qdrant(docs, source="case_log_excel", path=path)


def ingest_cases_csv(path: str = "data/case_log.csv") -> Dict[str, int]:
	docs = parse_csv_to_documents(path)
	if not docs:
		return {"rows": 0, "chunks": 0, "upserted": 0}
	return _upsert_docs_to_qdrant(docs, source="case_log_csv", path=path)
