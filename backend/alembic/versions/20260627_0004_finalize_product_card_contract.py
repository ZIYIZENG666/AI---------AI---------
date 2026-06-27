"""Finalize product card contract."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260627_0004"
down_revision: str | None = "20260623_0003"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "product_cards",
        sa.Column("source_type", sa.String(length=20), nullable=True),
    )
    op.execute(
        "UPDATE product_cards SET source_type = 'ai_generated' "
        "WHERE source_type IS NULL"
    )
    op.execute("DELETE FROM product_cards WHERE status = 'rejected'")

    op.alter_column(
        "product_cards",
        "source_type",
        existing_type=sa.String(length=20),
        nullable=False,
    )
    op.drop_constraint(
        "ck_product_cards_status_allowed",
        "product_cards",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_product_cards_status"),
        "product_cards",
        "status IN ('draft', 'confirmed')",
    )
    op.create_check_constraint(
        op.f("ck_product_cards_source_type"),
        "product_cards",
        "source_type IN ('ai_generated', 'manual')",
    )
    op.create_index(
        op.f("ix_product_cards_source_type"),
        "product_cards",
        ["source_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_product_cards_source_type"), table_name="product_cards")
    op.drop_constraint(
        op.f("ck_product_cards_source_type"),
        "product_cards",
        type_="check",
    )
    op.drop_constraint(
        op.f("ck_product_cards_status"),
        "product_cards",
        type_="check",
    )
    op.create_check_constraint(
        "ck_product_cards_status_allowed",
        "product_cards",
        "status IN ('draft', 'confirmed', 'rejected')",
    )
    op.drop_column("product_cards", "source_type")
