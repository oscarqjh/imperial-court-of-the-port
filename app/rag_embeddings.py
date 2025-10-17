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


def embed_texts(texts: List[str]) -> List[List[float]]:
	if not openai_available:
		raise RuntimeError("openai package not available; ensure requirements are installed")
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY is required for embedding")
	client = OpenAI(api_key=api_key)
	resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
	return [item.embedding for item in resp.data]
