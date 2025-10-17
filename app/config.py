from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	mock_mode: bool = True
	openai_api_key: str | None = None
	host: str = "0.0.0.0"
	port: int = 8000
	# Database
	supabase_db_url: str | None = None  # e.g. postgresql+asyncpg://user:pass@host:port/db
	db_pool_size: int = 5
	db_max_overflow: int = 10
	db_ssl_allow_self_signed: bool = False
	# Supabase client
	supabase_url: str | None = None
	supabase_anon_key: str | None = None
	supabase_service_role_key: str | None = None

	class Config:
		env_prefix = ""
		case_sensitive = False


settings = Settings()
