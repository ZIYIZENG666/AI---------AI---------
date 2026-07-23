"""ORM models for the qualification module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class LeadScore(Base):
    """AI customer-fit score for a validated Lead."""

    __tablename__ = "lead_scores"
    __table_args__ = (
        CheckConstraint(
            "fit_score >= 0 AND fit_score <= 100",
            name=conv("ck_lead_scores_fit_score"),
        ),
        CheckConstraint(
            "recommendation IN ('recommended', 'maybe', 'not_recommended', "
            "'needs_manual_review')",
            name=conv("ck_lead_scores_recommendation"),
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
    fit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    matching_reasons: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    risk_notes: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    uncertainty_notes: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    evidence: Mapped[list[dict]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    suggested_outreach_angle: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
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
