from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()


class Settings(BaseSettings):
	mock_mode: bool = False  # Default to False instead of True
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
	# Qdrant configuration
	qdrant_url: str | None = None
	qdrant_api_key: str | None = None
	qdrant_collection: str | None = None
	# Embedding configuration
	embed_model: str | None = None
	# CrewAI configuration
	crewai_tracing_enabled: bool = False
	# Celery configuration
	celery_broker_url: str | None = None

	class Config:
		env_prefix = ""
		case_sensitive = False
		env_file = ".env"  # Explicitly specify .env file
		extra = "allow"  # Allow extra fields from environment


settings = Settings()
