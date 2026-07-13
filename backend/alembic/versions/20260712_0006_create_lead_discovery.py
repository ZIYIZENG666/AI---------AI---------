"""Create Lead Discovery task and lead tables."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260712_0006"
down_revision: str | None = "20260703_0005"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "task_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("task_type", sa.String(length=50), nullable=False),
        sa.Column("related_entity_type", sa.String(length=50), nullable=False),
        sa.Column("related_entity_id", sa.String(length=36), nullable=False),
        sa.Column("search_query", sa.Text(), nullable=False),
        sa.Column("provider_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "task_type IN ('lead_discovery')",
            name=op.f("ck_task_runs_task_type"),
        ),
        sa.CheckConstraint(
            "related_entity_type IN ('campaign')",
            name=op.f("ck_task_runs_related_entity_type"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed', 'cancelled')",
            name=op.f("ck_task_runs_status"),
        ),
        sa.CheckConstraint(
            "progress >= 0 AND progress <= 100",
            name=op.f("ck_task_runs_progress"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_runs")),
    )
    op.create_index(
        op.f("ix_task_runs_related_entity_id"),
        "task_runs",
        ["related_entity_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_runs_status"),
        "task_runs",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_runs_task_type"),
        "task_runs",
        ["task_type"],
        unique=False,
    )

    op.create_table(
        "leads",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("campaign_id", sa.String(length=36), nullable=False),
        sa.Column("task_run_id", sa.String(length=36), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=2048), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("normalized_website", sa.String(length=512), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("country", sa.String(length=255), nullable=True),
        sa.Column("industry", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("search_query", sa.Text(), nullable=False),
        sa.Column("raw_snippet", sa.Text(), nullable=True),
        sa.Column("discovery_reason", sa.Text(), nullable=True),
        sa.Column("provider_name", sa.String(length=100), nullable=False),
        sa.Column("discovery_status", sa.String(length=20), nullable=False),
        sa.Column("validation_status", sa.String(length=30), nullable=False),
        sa.Column("review_status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "discovery_status IN ('discovered')",
            name=op.f("ck_leads_discovery_status"),
        ),
        sa.CheckConstraint(
            "validation_status IN ('pending', 'valid', 'invalid', 'duplicate', "
            "'insufficient_content')",
            name=op.f("ck_leads_validation_status"),
        ),
        sa.CheckConstraint(
            "review_status IN ('unreviewed', 'approved', 'rejected', "
            "'needs_manual_review')",
            name=op.f("ck_leads_review_status"),
        ),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["campaigns.id"],
            name=op.f("fk_leads_campaign_id_campaigns"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_run_id"],
            ["task_runs.id"],
            name=op.f("fk_leads_task_run_id_task_runs"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
        sa.UniqueConstraint(
            "campaign_id",
            "normalized_website",
            name=op.f("uq_leads_campaign_id_normalized_website"),
        ),
    )
    op.create_index(
        op.f("ix_leads_campaign_id"),
        "leads",
        ["campaign_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_discovery_status"),
        "leads",
        ["discovery_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_review_status"),
        "leads",
        ["review_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_task_run_id"),
        "leads",
        ["task_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_validation_status"),
        "leads",
        ["validation_status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_leads_validation_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_task_run_id"), table_name="leads")
    op.drop_index(op.f("ix_leads_review_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_discovery_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_campaign_id"), table_name="leads")
    op.drop_table("leads")

    op.drop_index(op.f("ix_task_runs_task_type"), table_name="task_runs")
    op.drop_index(op.f("ix_task_runs_status"), table_name="task_runs")
    op.drop_index(op.f("ix_task_runs_related_entity_id"), table_name="task_runs")
    op.drop_table("task_runs")
