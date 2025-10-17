from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	mock_mode: bool = True
	openai_api_key: str | None = None
	host: str = "0.0.0.0"
	port: int = 8000

	class Config:
		env_prefix = ""
		case_sensitive = False


settings = Settings()
