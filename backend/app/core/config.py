"""Environment-based backend settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


CONFIG_FILE = Path(__file__).resolve()
BACKEND_DIR = CONFIG_FILE.parents[2]
PROJECT_ROOT = CONFIG_FILE.parents[3]


class Settings(BaseSettings):
    """Typed settings loaded from environment variables."""

    app_name: str = "AI B2B Sales Knowledge Base & Lead Qualification System"
    app_env: str = "development"
    app_debug: bool = False
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 5173
    frontend_url: str = "http://localhost:5173"
    secret_key: str = ""
    cors_allowed_origins: str = "http://localhost:5173"

    database_url: str
    redis_url: str

    openai_api_key: str = ""
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_redirect_uri: str = ""
    search_api_key: str = ""
    crawler_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=(PROJECT_ROOT / ".env", BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()
