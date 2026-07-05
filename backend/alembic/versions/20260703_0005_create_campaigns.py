"""Create campaigns."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260703_0005"
down_revision: str | None = "20260627_0004"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("company_id", sa.String(length=36), nullable=False),
        sa.Column("product_card_id", sa.String(length=36), nullable=False),
        sa.Column("product_card_snapshot", sa.JSON(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("target_country", sa.String(length=255), nullable=True),
        sa.Column("target_region", sa.String(length=255), nullable=True),
        sa.Column("target_industry", sa.String(length=255), nullable=True),
        sa.Column("target_company_type", sa.String(length=255), nullable=True),
        sa.Column("target_role", sa.String(length=255), nullable=True),
        sa.Column("search_keywords", sa.JSON(), nullable=False),
        sa.Column("qualification_criteria", sa.JSON(), nullable=False),
        sa.Column("outreach_angle", sa.Text(), nullable=True),
        sa.Column("lead_limit", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'confirmed', 'archived')",
            name=op.f("ck_campaigns_status"),
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company_profiles.id"],
            name=op.f("fk_campaigns_company_id_company_profiles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_card_id"],
            ["product_cards.id"],
            name=op.f("fk_campaigns_product_card_id_product_cards"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_campaigns")),
    )
    op.create_index(
        op.f("ix_campaigns_company_id"),
        "campaigns",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_campaigns_product_card_id"),
        "campaigns",
        ["product_card_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_campaigns_status"),
        "campaigns",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_campaigns_status"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_product_card_id"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_company_id"), table_name="campaigns")
    op.drop_table("campaigns")
