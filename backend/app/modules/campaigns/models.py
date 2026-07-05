"""ORM models for the campaigns module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import conv

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class Campaign(Base):
    """Sales campaign configuration based on a confirmed product card."""

    __tablename__ = "campaigns"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'confirmed', 'archived')",
            name=conv("ck_campaigns_status"),
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
    product_card_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("product_cards.id"),
        nullable=False,
        index=True,
    )
    product_card_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_country: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_company_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    target_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    search_keywords: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    qualification_criteria: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    outreach_angle: Mapped[str | None] = mapped_column(Text, nullable=True)
    lead_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
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
