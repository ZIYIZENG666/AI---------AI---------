"""ORM models for the discovery module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class Lead(Base):
    """Candidate company discovered for a confirmed Campaign."""

    __tablename__ = "leads"
    __table_args__ = (
        CheckConstraint(
            "discovery_status IN ('discovered')",
            name=conv("ck_leads_discovery_status"),
        ),
        CheckConstraint(
            "validation_status IN ('pending', 'valid', 'invalid', 'duplicate', "
            "'insufficient_content')",
            name=conv("ck_leads_validation_status"),
        ),
        CheckConstraint(
            "review_status IN ('unreviewed', 'approved', 'rejected', "
            "'needs_manual_review')",
            name=conv("ck_leads_review_status"),
        ),
        UniqueConstraint(
            "campaign_id",
            "normalized_website",
            name=conv("uq_leads_campaign_id_normalized_website"),
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_run_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("task_runs.id"),
        nullable=False,
        index=True,
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str] = mapped_column(String(2048), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_website: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    country: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    search_query: Mapped[str] = mapped_column(Text, nullable=False)
    raw_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    discovery_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_name: Mapped[str] = mapped_column(String(100), nullable=False)
    discovery_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="discovered",
        index=True,
    )
    validation_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
        index=True,
    )
    review_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="unreviewed",
        index=True,
    )
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
