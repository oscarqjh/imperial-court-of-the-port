from __future__ import annotations

from typing import Any, List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_, or_, text
from sqlalchemy.orm import selectinload

from .db import get_session_factory
from .models import EdiMessage, ApiEvent, Container, Vessel, VesselAdvice, BerthApplication
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


# === COMPREHENSIVE DATABASE TOOLS FOR AI AGENTS ===

async def get_vessel_operations_summary() -> Dict[str, Any]:
	"""Get summary of vessel operations for decision making."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		# Count vessels by status/location
		vessel_count = await session.execute(select(func.count(Vessel.vessel_id)))
		total_vessels = vessel_count.scalar()
		
		# Container status distribution
		container_stats = await session.execute(
			select(Container.status, func.count(Container.container_id))
			.group_by(Container.status)
		)
		status_counts = {status: count for status, count in container_stats.all()}
		
		# Recent EDI message activity (last 24 hours)
		yesterday = datetime.utcnow() - timedelta(days=1)
		recent_edi = await session.execute(
			select(func.count(EdiMessage.edi_id))
			.where(EdiMessage.sent_at >= yesterday)
		)
		recent_edi_count = recent_edi.scalar()
		
		# Active vessel advice
		active_advice = await session.execute(
			select(func.count(VesselAdvice.vessel_advice_no))
			.where(VesselAdvice.effective_end_datetime.is_(None))
		)
		active_advice_count = active_advice.scalar()
		
		return {
			"total_vessels": total_vessels,
			"container_status_distribution": status_counts,
			"recent_edi_activity_24h": recent_edi_count,
			"active_vessel_advice": active_advice_count,
			"timestamp": datetime.utcnow().isoformat()
		}


async def search_containers_by_criteria(
	container_no: Optional[str] = None,
	status: Optional[str] = None,
	vessel_name: Optional[str] = None,
	port_code: Optional[str] = None,
	limit: int = 10
) -> List[Dict[str, Any]]:
	"""Search containers by various criteria for incident analysis."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		query = select(Container).options(selectinload(Container.vessel))
		
		conditions = []
		if container_no:
			conditions.append(Container.cntr_no.ilike(f"%{container_no}%"))
		if status:
			conditions.append(Container.status == status)
		if port_code:
			conditions.append(or_(
				Container.origin_port == port_code,
				Container.tranship_port == port_code,
				Container.destination_port == port_code
			))
		if vessel_name:
			query = query.join(Vessel).where(Vessel.vessel_name.ilike(f"%{vessel_name}%"))
		
		if conditions:
			query = query.where(and_(*conditions))
		
		query = query.limit(limit)
		result = await session.execute(query)
		containers = result.scalars().all()
		
		return [
			{
				"container_id": c.container_id,
				"cntr_no": c.cntr_no,
				"status": c.status,
				"size_type": c.size_type,
				"gross_weight_kg": float(c.gross_weight_kg) if c.gross_weight_kg else None,
				"origin_port": c.origin_port,
				"tranship_port": c.tranship_port,
				"destination_port": c.destination_port,
				"vessel_name": c.vessel.vessel_name if c.vessel else None,
				"eta_ts": c.eta_ts.isoformat() if c.eta_ts else None,
				"etd_ts": c.etd_ts.isoformat() if c.etd_ts else None,
				"last_free_day": c.last_free_day.isoformat() if c.last_free_day else None,
			}
			for c in containers
		]


async def get_edi_message_analysis(
	message_type: Optional[str] = None,
	status: Optional[str] = None,
	hours_back: int = 24,
	limit: int = 20
) -> Dict[str, Any]:
	"""Analyze EDI messages for system health and issues."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
		
		query = select(EdiMessage).where(EdiMessage.sent_at >= cutoff_time)
		
		if message_type:
			query = query.where(EdiMessage.message_type == message_type)
		if status:
			query = query.where(EdiMessage.status == status)
		
		query = query.order_by(desc(EdiMessage.sent_at)).limit(limit)
		result = await session.execute(query)
		messages = result.scalars().all()
		
		# Error analysis
		error_query = select(EdiMessage).where(
			and_(
				EdiMessage.sent_at >= cutoff_time,
				EdiMessage.status == 'ERROR'
			)
		)
		error_result = await session.execute(error_query)
		error_messages = error_result.scalars().all()
		
		# Status distribution
		status_query = select(
			EdiMessage.status, 
			func.count(EdiMessage.edi_id)
		).where(EdiMessage.sent_at >= cutoff_time).group_by(EdiMessage.status)
		status_result = await session.execute(status_query)
		status_distribution = {status: count for status, count in status_result.all()}
		
		return {
			"messages": [
				{
					"edi_id": msg.edi_id,
					"message_type": msg.message_type,
					"direction": msg.direction,
					"status": msg.status,
					"sender": msg.sender,
					"receiver": msg.receiver,
					"sent_at": msg.sent_at.isoformat(),
					"error_text": msg.error_text
				}
				for msg in messages
			],
			"error_messages": [
				{
					"edi_id": err.edi_id,
					"message_type": err.message_type,
					"error_text": err.error_text,
					"sent_at": err.sent_at.isoformat()
				}
				for err in error_messages
			],
			"status_distribution": status_distribution,
			"analysis_period_hours": hours_back,
			"total_messages": len(messages),
			"error_count": len(error_messages)
		}


async def get_vessel_by_name_or_imo(
	vessel_name: Optional[str] = None,
	imo_no: Optional[int] = None
) -> Optional[Dict[str, Any]]:
	"""Get detailed vessel information by name or IMO number."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		query = select(Vessel).options(
			selectinload(Vessel.containers),
			selectinload(Vessel.edi_messages),
			selectinload(Vessel.api_events)
		)
		
		if vessel_name:
			query = query.where(Vessel.vessel_name.ilike(f"%{vessel_name}%"))
		elif imo_no:
			query = query.where(Vessel.imo_no == imo_no)
		else:
			return None
		
		result = await session.execute(query)
		vessel = result.scalars().first()
		
		if not vessel:
			return None
		
		return {
			"vessel_id": vessel.vessel_id,
			"imo_no": vessel.imo_no,
			"vessel_name": vessel.vessel_name,
			"call_sign": vessel.call_sign,
			"operator_name": vessel.operator_name,
			"flag_state": vessel.flag_state,
			"built_year": vessel.built_year,
			"capacity_teu": vessel.capacity_teu,
			"loa_m": float(vessel.loa_m) if vessel.loa_m else None,
			"beam_m": float(vessel.beam_m) if vessel.beam_m else None,
			"draft_m": float(vessel.draft_m) if vessel.draft_m else None,
			"last_port": vessel.last_port,
			"next_port": vessel.next_port,
			"container_count": len(vessel.containers),
			"recent_edi_count": len([m for m in vessel.edi_messages if m.sent_at >= datetime.utcnow() - timedelta(hours=24)]),
			"recent_api_events": len([e for e in vessel.api_events if e.event_ts >= datetime.utcnow() - timedelta(hours=24)])
		}


async def get_container_operational_status(container_no: str) -> Optional[Dict[str, Any]]:
	"""Get detailed operational status of a specific container."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		query = select(Container).options(
			selectinload(Container.vessel)
		).where(Container.cntr_no == container_no)
		
		result = await session.execute(query)
		container = result.scalars().first()
		
		if not container:
			return None
		
		# Get related EDI messages
		edi_query = select(EdiMessage).where(
			EdiMessage.container_id == container.container_id
		).order_by(desc(EdiMessage.sent_at)).limit(5)
		edi_result = await session.execute(edi_query)
		edi_messages = edi_result.scalars().all()
		
		# Get related API events
		api_query = select(ApiEvent).where(
			ApiEvent.container_id == container.container_id
		).order_by(desc(ApiEvent.event_ts)).limit(5)
		api_result = await session.execute(api_query)
		api_events = api_result.scalars().all()
		
		return {
			"container": {
				"cntr_no": container.cntr_no,
				"status": container.status,
				"size_type": container.size_type,
				"gross_weight_kg": float(container.gross_weight_kg) if container.gross_weight_kg else None,
				"origin_port": container.origin_port,
				"tranship_port": container.tranship_port,
				"destination_port": container.destination_port,
				"hazard_class": container.hazard_class,
				"eta_ts": container.eta_ts.isoformat() if container.eta_ts else None,
				"etd_ts": container.etd_ts.isoformat() if container.etd_ts else None,
				"last_free_day": container.last_free_day.isoformat() if container.last_free_day else None,
			},
			"vessel": {
				"vessel_name": container.vessel.vessel_name if container.vessel else None,
				"imo_no": container.vessel.imo_no if container.vessel else None,
				"operator_name": container.vessel.operator_name if container.vessel else None,
			} if container.vessel else None,
			"recent_edi_messages": [
				{
					"message_type": msg.message_type,
					"status": msg.status,
					"sent_at": msg.sent_at.isoformat(),
					"error_text": msg.error_text
				}
				for msg in edi_messages
			],
			"recent_api_events": [
				{
					"event_type": event.event_type,
					"source_system": event.source_system,
					"event_ts": event.event_ts.isoformat(),
					"http_status": event.http_status
				}
				for event in api_events
			]
		}


async def get_system_health_metrics() -> Dict[str, Any]:
	"""Get overall system health metrics for operational assessment."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		now = datetime.utcnow()
		one_hour_ago = now - timedelta(hours=1)
		one_day_ago = now - timedelta(days=1)
		
		# EDI message health
		edi_last_hour = await session.execute(
			select(func.count(EdiMessage.edi_id))
			.where(EdiMessage.sent_at >= one_hour_ago)
		)
		
		edi_errors_last_hour = await session.execute(
			select(func.count(EdiMessage.edi_id))
			.where(and_(
				EdiMessage.sent_at >= one_hour_ago,
				EdiMessage.status == 'ERROR'
			))
		)
		
		# API event health
		api_events_last_hour = await session.execute(
			select(func.count(ApiEvent.api_id))
			.where(ApiEvent.event_ts >= one_hour_ago)
		)
		
		api_errors_last_hour = await session.execute(
			select(func.count(ApiEvent.api_id))
			.where(and_(
				ApiEvent.event_ts >= one_hour_ago,
				ApiEvent.http_status >= 400
			))
		)
		
		# Container operation metrics
		containers_in_operation = await session.execute(
			select(func.count(Container.container_id))
			.where(Container.status.in_(['TRANSHIP', 'IN_YARD', 'ON_VESSEL', 'LOADED']))
		)
		
		# Recent vessel advice
		active_vessel_advice = await session.execute(
			select(func.count(VesselAdvice.vessel_advice_no))
			.where(VesselAdvice.effective_end_datetime.is_(None))
		)
		
		return {
			"timestamp": now.isoformat(),
			"edi_health": {
				"messages_last_hour": edi_last_hour.scalar(),
				"errors_last_hour": edi_errors_last_hour.scalar(),
				"error_rate_percent": round((edi_errors_last_hour.scalar() / max(1, edi_last_hour.scalar())) * 100, 2)
			},
			"api_health": {
				"events_last_hour": api_events_last_hour.scalar(),
				"errors_last_hour": api_errors_last_hour.scalar(),
				"error_rate_percent": round((api_errors_last_hour.scalar() / max(1, api_events_last_hour.scalar())) * 100, 2)
			},
			"operations": {
				"containers_in_operation": containers_in_operation.scalar(),
				"active_vessel_advice": active_vessel_advice.scalar()
			}
		}


async def search_recent_issues(
	keywords: List[str],
	hours_back: int = 48,
	include_edi_errors: bool = True,
	include_api_errors: bool = True
) -> Dict[str, Any]:
	"""Search for recent issues based on keywords in error messages."""
	session_factory = get_session_factory()
	async with session_factory() as session:
		cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
		issues = []
		
		if include_edi_errors:
			# Search EDI error messages
			for keyword in keywords:
				edi_query = select(EdiMessage).where(and_(
					EdiMessage.sent_at >= cutoff_time,
					EdiMessage.status == 'ERROR',
					EdiMessage.error_text.ilike(f"%{keyword}%")
				)).order_by(desc(EdiMessage.sent_at)).limit(10)
				
				edi_result = await session.execute(edi_query)
				edi_issues = edi_result.scalars().all()
				
				for issue in edi_issues:
					issues.append({
						"type": "EDI_ERROR",
						"timestamp": issue.sent_at.isoformat(),
						"message_type": issue.message_type,
						"error_text": issue.error_text,
						"sender": issue.sender,
						"receiver": issue.receiver,
						"keyword_matched": keyword
					})
		
		if include_api_errors:
			# Search API errors (HTTP status >= 400)
			api_query = select(ApiEvent).where(and_(
				ApiEvent.event_ts >= cutoff_time,
				ApiEvent.http_status >= 400
			)).order_by(desc(ApiEvent.event_ts)).limit(20)
			
			api_result = await session.execute(api_query)
			api_issues = api_result.scalars().all()
			
			for issue in api_issues:
				issues.append({
					"type": "API_ERROR",
					"timestamp": issue.event_ts.isoformat(),
					"event_type": issue.event_type,
					"source_system": issue.source_system,
					"http_status": issue.http_status,
					"correlation_id": issue.correlation_id
				})
		
		# Sort all issues by timestamp (most recent first)
		issues.sort(key=lambda x: x["timestamp"], reverse=True)
		
		return {
			"search_keywords": keywords,
			"search_period_hours": hours_back,
			"total_issues_found": len(issues),
			"issues": issues[:50]  # Limit to 50 most recent
		}
