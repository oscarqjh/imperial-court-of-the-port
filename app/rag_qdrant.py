from __future__ import annotations

from typing import List, Dict, Any, Optional
import os

from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels


DEFAULT_COLLECTION = os.getenv("QDRANT_COLLECTION", "imperial_court_kb")


class QdrantStore:
	def __init__(self, collection: str = DEFAULT_COLLECTION) -> None:
		api_url = os.getenv("QDRANT_URL")
		api_key = os.getenv("QDRANT_API_KEY")
		if not api_url:
			raise RuntimeError("QDRANT_URL is required (create a free cluster in Qdrant Cloud)")
		self.client = QdrantClient(url=api_url, api_key=api_key, timeout=60.0)
		self.collection = collection
		self._ensure_collection()

	def _ensure_collection(self) -> None:
		exists = False
		try:
			collections = self.client.get_collections().collections
			exists = any(c.name == self.collection for c in collections)
		except Exception:
			logger.exception("Failed to list collections")
		if exists:
			return
		logger.info(f"Creating Qdrant collection: {self.collection}")
		self.client.create_collection(
			collection_name=self.collection,
			vectors_config=qmodels.VectorParams(size=1536, distance=qmodels.Distance.COSINE),
		)

	def upsert(self, ids: List[str], vectors: List[List[float]], payloads: List[Dict[str, Any]]) -> None:
		assert len(ids) == len(vectors) == len(payloads)
		self.client.upsert(
			collection_name=self.collection,
			points=[qmodels.PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))],
		)

	def search(self, vector: List[float], top_k: int = 5, filter_: Optional[qmodels.Filter] = None) -> List[Dict[str, Any]]:
		res = self.client.search(collection_name=self.collection, query_vector=vector, limit=top_k, query_filter=filter_)
		out: List[Dict[str, Any]] = []
		for p in res:
			out.append({
				"id": str(p.id),
				"score": p.score,
				"text": p.payload.get("text", ""),
				"meta": {k: v for k, v in p.payload.items() if k != "text"},
			})
		return out
