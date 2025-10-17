from __future__ import annotations

from typing import Any, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from .db import get_session_factory
from .models import EdiMessage, ApiEvent
from .supabase_client import get_supabase_client


async def list_recent_edi_messages_orm(limit: int = 10) -> List[Dict[str, Any]]:
	"""List recent EDI messages using ORM (preferred for consistency with init_orm)."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		stmt = select(EdiMessage).order_by(desc(EdiMessage.sent_at)).limit(limit)
		result = await session.execute(stmt)
		messages = result.scalars().all()
		return [
			{
				"edi_id": msg.edi_id,
				"container_id": msg.container_id,
				"vessel_id": msg.vessel_id,
				"message_type": msg.message_type,
				"direction": msg.direction,
				"status": msg.status,
				"message_ref": msg.message_ref,
				"sender": msg.sender,
				"receiver": msg.receiver,
				"sent_at": msg.sent_at,
				"ack_at": msg.ack_at,
				"error_text": msg.error_text,
				"created_at": msg.created_at,
			}
			for msg in messages
		]


async def insert_api_event_orm(event: Dict[str, Any]) -> Dict[str, Any]:
	"""Insert API event using ORM (preferred for consistency with init_orm)."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		api_event = ApiEvent(**event)
		session.add(api_event)
		await session.commit()
		await session.refresh(api_event)
		return {
			"api_id": api_event.api_id,
			"container_id": api_event.container_id,
			"vessel_id": api_event.vessel_id,
			"event_type": api_event.event_type,
			"source_system": api_event.source_system,
			"http_status": api_event.http_status,
			"correlation_id": api_event.correlation_id,
			"event_ts": api_event.event_ts,
			"payload_json": api_event.payload_json,
			"created_at": api_event.created_at,
		}


# Legacy Supabase client functions (keep for backward compatibility)
def list_recent_edi_messages(limit: int = 10) -> List[Dict[str, Any]]:
	"""List recent EDI messages using Supabase client (legacy)."""
	sb = get_supabase_client()
	res = sb.table("edi_message").select("*").order("sent_at", desc=True).limit(limit).execute()
	return res.data or []


def insert_api_event(event: Dict[str, Any]) -> Dict[str, Any]:
	"""Insert API event using Supabase client (legacy)."""
	sb = get_supabase_client()
	res = sb.table("api_event").insert(event).execute()
	rows = res.data or []
	return rows[0] if rows else {}
