"""Create company sources and knowledge items."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0002"
down_revision: str | None = "20260622_0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "company_sources",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("company_id", sa.String(length=36), nullable=False),
        sa.Column("source_type", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("raw_content", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "source_type IN ('text', 'url')",
            name="ck_company_sources_source_type_allowed",
        ),
        sa.CheckConstraint(
            "status IN ('ready')",
            name="ck_company_sources_status_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company_profiles.id"],
            name=op.f("fk_company_sources_company_id_company_profiles"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_company_sources")),
    )
    op.create_index(
        op.f("ix_company_sources_company_id"),
        "company_sources",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_company_sources_status"),
        "company_sources",
        ["status"],
        unique=False,
    )

    op.create_table(
        "knowledge_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("company_id", sa.String(length=36), nullable=False),
        sa.Column("source_id", sa.String(length=36), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'confirmed', 'rejected')",
            name="ck_knowledge_items_status_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company_profiles.id"],
            name=op.f("fk_knowledge_items_company_id_company_profiles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["company_sources.id"],
            name=op.f("fk_knowledge_items_source_id_company_sources"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_knowledge_items")),
    )
    op.create_index(
        op.f("ix_knowledge_items_company_id"),
        "knowledge_items",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_items_source_id"),
        "knowledge_items",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_items_status"),
        "knowledge_items",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_knowledge_items_status"), table_name="knowledge_items")
    op.drop_index(op.f("ix_knowledge_items_source_id"), table_name="knowledge_items")
    op.drop_index(op.f("ix_knowledge_items_company_id"), table_name="knowledge_items")
    op.drop_table("knowledge_items")

    op.drop_index(op.f("ix_company_sources_status"), table_name="company_sources")
    op.drop_index(op.f("ix_company_sources_company_id"), table_name="company_sources")
    op.drop_table("company_sources")
