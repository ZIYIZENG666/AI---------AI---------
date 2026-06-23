"""ORM models for the product card module."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utcnow() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class ProductCard(Base):
    """Structured product information generated from confirmed knowledge."""

    __tablename__ = "product_cards"
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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_customer: Mapped[str] = mapped_column(Text, nullable=False)
    pain_points: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    value_proposition: Mapped[str] = mapped_column(Text, nullable=False)
    use_cases: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    differentiators: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    source_knowledge_item_ids: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
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
