"""ORM models for the intelligence module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class LeadIntelligence(Base):
    """Factual website intelligence captured during Lead Validation."""

    __tablename__ = "lead_intelligence"
    __table_args__ = (
        CheckConstraint(
            "crawl_status IN ('completed', 'failed', 'insufficient_content', 'skipped')",
            name=conv("ck_lead_intelligence_crawl_status"),
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    lead_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_run_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("task_runs.id"),
        nullable=False,
        index=True,
    )
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(100), nullable=False)
    website_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    products_or_services: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    target_customers: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    business_model: Mapped[str | None] = mapped_column(Text, nullable=True)
    pain_points: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    evidence: Mapped[list[dict]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    content_quality: Mapped[str] = mapped_column(String(50), nullable=False)
    crawl_status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
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
