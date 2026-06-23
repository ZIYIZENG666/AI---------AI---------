from app.core.config import get_settings


def test_settings_read_environment_values(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/testdb")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6380/2")
    monkeypatch.setenv("APP_ENV", "test")

    get_settings.cache_clear()
    settings = get_settings()

    assert settings.database_url == "postgresql+psycopg://user:pass@localhost:5432/testdb"
    assert settings.redis_url == "redis://localhost:6380/2"
    assert settings.app_env == "test"

    get_settings.cache_clear()
