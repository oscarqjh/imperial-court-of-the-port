from __future__ import annotations

from typing import List
import os

from loguru import logger

try:
	from openai import OpenAI
	openai_available = True
except Exception:
	openai_available = False


EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")


def _batched(items: List[str], batch_size: int) -> List[List[str]]:
	return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def embed_texts(texts: List[str]) -> List[List[float]]:
	if not openai_available:
		raise RuntimeError("openai package not available; ensure requirements are installed")
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY is required for embedding")

	# sanitize inputs: ensure non-empty strings
	clean_texts: List[str] = []
	index_map: List[int] = []
	for idx, t in enumerate(texts):
		if not isinstance(t, str):
			continue
		s = t.strip()
		if not s:
			continue
		clean_texts.append(s)
		index_map.append(idx)
	if not clean_texts:
		raise ValueError("No non-empty text chunks to embed")

	client = OpenAI(api_key=api_key)
	embeddings: List[List[float]] = []
	for batch in _batched(clean_texts, batch_size=100):
		try:
			resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
			embeddings.extend([item.embedding for item in resp.data])
		except Exception as e:
			logger.exception("Embedding batch failed")
			raise

	# Re-expand to original order; callers using filtered indices should align accordingly
	return embeddings
