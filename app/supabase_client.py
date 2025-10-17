from __future__ import annotations

from typing import Optional

from loguru import logger

try:
	from supabase import create_client, Client  # type: ignore
	has_supabase = True
except Exception:
	has_supabase = False
	Client = object  # type: ignore

from .config import settings


_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
	global _supabase_client
	if not has_supabase:
		raise RuntimeError("supabase package not installed")
	if _supabase_client is None:
		url = settings.supabase_url
		key = settings.supabase_service_role_key or settings.supabase_anon_key
		if not url or not key:
			raise RuntimeError("SUPABASE_URL and a key (service role or anon) are required")
		logger.info("Initializing Supabase client")
		_supabase_client = create_client(url, key)
	return _supabase_client
