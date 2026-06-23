"""Create product cards."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0003"
down_revision: str | None = "20260623_0002"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "product_cards",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("company_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("target_customer", sa.Text(), nullable=False),
        sa.Column("pain_points", sa.JSON(), nullable=False),
        sa.Column("value_proposition", sa.Text(), nullable=False),
        sa.Column("use_cases", sa.JSON(), nullable=False),
        sa.Column("differentiators", sa.JSON(), nullable=False),
        sa.Column("source_knowledge_item_ids", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'confirmed', 'rejected')",
            name="ck_product_cards_status_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company_profiles.id"],
            name=op.f("fk_product_cards_company_id_company_profiles"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_cards")),
    )
    op.create_index(
        op.f("ix_product_cards_company_id"),
        "product_cards",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_cards_status"),
        "product_cards",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_product_cards_status"), table_name="product_cards")
    op.drop_index(op.f("ix_product_cards_company_id"), table_name="product_cards")
    op.drop_table("product_cards")
