from __future__ import annotations

from typing import Any, List, Dict

from .supabase_client import get_supabase_client


def list_recent_edi_messages(limit: int = 10) -> List[Dict[str, Any]]:
	sb = get_supabase_client()
	res = sb.table("edi_message").select("*").order("sent_at", desc=True).limit(limit).execute()
	return res.data or []


def insert_api_event(event: Dict[str, Any]) -> Dict[str, Any]:
	sb = get_supabase_client()
	res = sb.table("api_event").insert(event).execute()
	rows = res.data or []
	return rows[0] if rows else {}
