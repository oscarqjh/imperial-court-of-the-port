from __future__ import annotations

from typing import AsyncIterator
import ssl
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from .config import settings

try:
	import certifi  # type: ignore
	has_certifi = True
except Exception:
	has_certifi = False


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def reset_engine() -> None:
	"""Reset the database engine and session factory to avoid prepared statement conflicts."""
	global _engine, _session_factory
	if _engine is not None:
		# Close existing engine
		_engine.sync_engine.dispose()
	_engine = None
	_session_factory = None


def _build_ssl_context() -> ssl.SSLContext:
	ctx = ssl.create_default_context()
	if has_certifi:
		ctx.load_verify_locations(cafile=certifi.where())
	if settings.db_ssl_allow_self_signed:
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
	return ctx


def _using_pgbouncer(url: str) -> bool:
	parts = urlparse(url)
	return ("pooler" in (parts.hostname or "")) or (parts.port == 6543)


def _add_query_param(url: str, key: str, value: str) -> str:
	parts = urlparse(url)
	pairs = parse_qsl(parts.query, keep_blank_values=True)
	if not any(k.lower() == key.lower() for k, _ in pairs):
		pairs.append((key, value))
	new_query = urlencode(pairs)
	return urlunparse((parts.scheme, parts.netloc, parts.path, parts.params, new_query, parts.fragment))


def _to_sqlalchemy_url(url: str) -> str:
	parts = urlparse(url)
	base = f"{parts.username}:{parts.password}@{parts.hostname}:{parts.port}{parts.path}"
	if _using_pgbouncer(url):
		return f"postgresql+psycopg://{base}?{parts.query}" if parts.query else f"postgresql+psycopg://{base}"
	return f"postgresql+asyncpg://{base}?{parts.query}" if parts.query else f"postgresql+asyncpg://{base}"


def get_engine() -> AsyncEngine:
	global _engine
	if _engine is None:
		if not settings.supabase_db_url:
			raise RuntimeError("SUPABASE_DB_URL is not configured")
		raw_url = settings.supabase_db_url

		if _using_pgbouncer(raw_url):
			# psycopg async: ensure sslmode=require in URL, no 'ssl' connect_arg
			url_with_sslmode = _add_query_param(raw_url, "sslmode", "require")
			sqlalchemy_url = _to_sqlalchemy_url(url_with_sslmode)
			_engine = create_async_engine(
				sqlalchemy_url,
				echo=False,
				poolclass=NullPool,
				connect_args={
					"prepare_threshold": None,  # Disable prepared statements
				},
			)
		else:
			# asyncpg: remove sslmode from URL (we pass SSL context via connect_args)
			parts = urlparse(raw_url)
			pairs = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() != "sslmode"]
			asyncpg_url = urlunparse((parts.scheme, parts.netloc, parts.path, parts.params, urlencode(pairs), parts.fragment))
			sqlalchemy_url = _to_sqlalchemy_url(asyncpg_url)
			ssl_ctx = _build_ssl_context()
			_engine = create_async_engine(
				sqlalchemy_url,
				pool_size=settings.db_pool_size,
				max_overflow=settings.db_max_overflow,
				echo=False,
				connect_args={
					"ssl": ssl_ctx,
					"statement_cache_size": 0,
					"prepared_statement_cache_size": 0,
				},
			)
	return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
	global _session_factory
	if _session_factory is None:
		_session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
	return _session_factory


async def run_sql_script(sql_text: str) -> None:
	engine = get_engine()
	async with engine.begin() as conn:
		await conn.execute(text(sql_text))


async def execute_query(sql: str) -> list[dict]:
	engine = get_engine()
	async with engine.connect() as conn:
		res = await conn.execute(text(sql))
		rows = res.mappings().all()
		return [dict(r) for r in rows]
