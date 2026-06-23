"""ORM models for the knowledge module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class KnowledgeItem(Base):
    """Reviewable company knowledge generated from source material."""

    __tablename__ = "knowledge_items"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'confirmed', 'rejected')",
            name="status_allowed",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    company_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("company_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("company_sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        index=True,
    )
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )
