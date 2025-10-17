from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .db import get_engine
from .models import Base
from .seed import seed_vessels, seed_extras

router = APIRouter(prefix="/db", tags=["db"])


class InitResponse(BaseModel):
	applied: bool


POSTGRES_VIEWS_DROP = """
DROP VIEW IF EXISTS vw_edi_last CASCADE;
DROP VIEW IF EXISTS vw_tranship_pipeline CASCADE;
"""

POSTGRES_VIEWS_CREATE = """
CREATE VIEW vw_tranship_pipeline AS
SELECT
  c.cntr_no,
  c.size_type,
  c.status,
  c.origin_port,
  c.tranship_port,
  c.destination_port,
  v.vessel_name,
  v.imo_no,
  c.eta_ts,
  c.etd_ts,
  c.last_free_day
FROM container c
LEFT JOIN vessel v ON v.vessel_id = c.vessel_id;

CREATE VIEW vw_edi_last AS
WITH last_edi AS (
  SELECT e.container_id, e.message_type, e.status, e.sent_at,
         ROW_NUMBER() OVER (PARTITION BY e.container_id ORDER BY e.sent_at DESC) AS rn
  FROM edi_message e
)
SELECT c.cntr_no,
       l.sent_at AS last_edi_time,
       l.message_type AS last_edi_type,
       l.status AS last_edi_status
FROM last_edi l
JOIN container c ON c.container_id = l.container_id
WHERE l.rn = 1;
"""


class QueryRequest(BaseModel):
	query: str


class QueryResponse(BaseModel):
	rows: list[dict]


class InsertRequest(BaseModel):
	table: str
	json: list[dict] | dict


class ListRequest(BaseModel):
	table: str
	limit: int = 10


class ListResponse(BaseModel):
	rows: list[dict]


def _split_statements(sql: str) -> list[str]:
	parts: list[str] = []
	buf: list[str] = []
	for line in sql.splitlines():
		buf.append(line)
		if line.strip().endswith(";"):
			parts.append("\n".join(buf))
			buf = []
	if buf:
		parts.append("\n".join(buf))
	return parts


@router.post("/init", response_model=InitResponse)
async def init_db() -> InitResponse:
	try:
		with open("data/Database/db.sql", "r", encoding="utf-8") as f:
			sql_text = f.read()
		pg_sql = transform_mysql_to_postgres(sql_text)
		for stmt in _split_statements(pg_sql):
			if stmt.strip():
				await run_sql_script(stmt)
		return InitResponse(applied=True)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/init_orm", response_model=InitResponse)
async def init_db_orm() -> InitResponse:
	try:
		engine = get_engine()
		async with engine.begin() as conn:
			# Drop views first to avoid dependency errors
			await conn.execute(text(POSTGRES_VIEWS_DROP))
			# Drop and create tables
			await conn.run_sync(Base.metadata.drop_all)
			await conn.run_sync(Base.metadata.create_all)
			# Recreate views
			await conn.execute(text(POSTGRES_VIEWS_CREATE))
		async with AsyncSession(engine) as session:
			await seed_vessels(session)
			await seed_extras(session)
			await session.commit()
		return InitResponse(applied=True)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def run_query(req: QueryRequest) -> QueryResponse:
	try:
		rows = await execute_query(req.query)
		return QueryResponse(rows=rows)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/sb/insert", response_model=QueryResponse)
async def sb_insert(req: InsertRequest) -> QueryResponse:
	try:
		sb = get_supabase_client()
		data = sb.table(req.table).insert(req.json).execute()
		rows = data.data or []
		return QueryResponse(rows=rows)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.post("/sb/list", response_model=ListResponse)
async def sb_list(req: ListRequest) -> ListResponse:
	try:
		sb = get_supabase_client()
		res = sb.table(req.table).select("*").limit(req.limit).execute()
		rows = res.data or []
		return ListResponse(rows=rows)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
