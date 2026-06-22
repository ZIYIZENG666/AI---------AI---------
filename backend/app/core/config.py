"""Minimal environment-based settings for the backend."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Small settings surface for the initial project skeleton."""

    app_env: str = "development"
    backend_port: int = 8000
    frontend_port: int = 5173
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ai_b2b_sales"
    )
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    search_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()
