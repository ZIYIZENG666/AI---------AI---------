"""Create Lead Validation and intelligence schema."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260714_0007"
down_revision: str | None = "20260712_0006"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "task_runs",
        sa.Column("input_url", sa.String(length=2048), nullable=True),
    )
    op.alter_column(
        "task_runs",
        "search_query",
        existing_type=sa.Text(),
        nullable=True,
    )
    op.drop_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        type_="check",
    )
    op.drop_constraint(
        op.f("ck_task_runs_related_entity_type"),
        "task_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        "task_type IN ('lead_discovery', 'lead_validation')",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_related_entity_type"),
        "task_runs",
        "related_entity_type IN ('campaign', 'lead')",
    )

    op.create_table(
        "lead_intelligence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("lead_id", sa.String(length=36), nullable=False),
        sa.Column("task_run_id", sa.String(length=36), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("provider_name", sa.String(length=100), nullable=False),
        sa.Column("website_summary", sa.Text(), nullable=True),
        sa.Column("products_or_services", sa.JSON(), nullable=False),
        sa.Column("target_customers", sa.JSON(), nullable=False),
        sa.Column("business_model", sa.Text(), nullable=True),
        sa.Column("pain_points", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("content_quality", sa.String(length=50), nullable=False),
        sa.Column("crawl_status", sa.String(length=30), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "crawl_status IN ('completed', 'failed', 'insufficient_content', 'skipped')",
            name=op.f("ck_lead_intelligence_crawl_status"),
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name=op.f("fk_lead_intelligence_lead_id_leads"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_run_id"],
            ["task_runs.id"],
            name=op.f("fk_lead_intelligence_task_run_id_task_runs"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead_intelligence")),
    )
    op.create_index(
        op.f("ix_lead_intelligence_crawl_status"),
        "lead_intelligence",
        ["crawl_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lead_intelligence_lead_id"),
        "lead_intelligence",
        ["lead_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lead_intelligence_task_run_id"),
        "lead_intelligence",
        ["task_run_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_lead_intelligence_task_run_id"),
        table_name="lead_intelligence",
    )
    op.drop_index(op.f("ix_lead_intelligence_lead_id"), table_name="lead_intelligence")
    op.drop_index(
        op.f("ix_lead_intelligence_crawl_status"),
        table_name="lead_intelligence",
    )
    op.drop_table("lead_intelligence")

    op.execute("DELETE FROM task_runs WHERE task_type = 'lead_validation'")
    op.drop_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        type_="check",
    )
    op.drop_constraint(
        op.f("ck_task_runs_related_entity_type"),
        "task_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        "task_type IN ('lead_discovery')",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_related_entity_type"),
        "task_runs",
        "related_entity_type IN ('campaign')",
    )
    op.drop_column("task_runs", "input_url")
    op.alter_column(
        "task_runs",
        "search_query",
        existing_type=sa.Text(),
        nullable=False,
    )
