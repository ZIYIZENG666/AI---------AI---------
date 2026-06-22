"""Database connection placeholders for future SQLAlchemy models."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


class Base(DeclarativeBase):
    """Declarative base for future ORM models."""


def get_db() -> Generator[Session, None, None]:
    """Yield a database session without binding any business models yet."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
