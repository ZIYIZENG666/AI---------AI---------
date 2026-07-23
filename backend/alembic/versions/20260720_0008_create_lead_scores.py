"""Create Lead Scoring schema."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260720_0008"
down_revision: str | None = "20260714_0007"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        "task_type IN ('lead_discovery', 'lead_validation', 'lead_scoring')",
    )

    op.create_table(
        "lead_scores",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("lead_id", sa.String(length=36), nullable=False),
        sa.Column("campaign_id", sa.String(length=36), nullable=False),
        sa.Column("task_run_id", sa.String(length=36), nullable=False),
        sa.Column("fit_score", sa.Integer(), nullable=False),
        sa.Column("recommendation", sa.String(length=30), nullable=False),
        sa.Column("matching_reasons", sa.JSON(), nullable=False),
        sa.Column("risk_notes", sa.JSON(), nullable=False),
        sa.Column("uncertainty_notes", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("suggested_outreach_angle", sa.Text(), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "fit_score >= 0 AND fit_score <= 100",
            name=op.f("ck_lead_scores_fit_score"),
        ),
        sa.CheckConstraint(
            "recommendation IN ('recommended', 'maybe', 'not_recommended', "
            "'needs_manual_review')",
            name=op.f("ck_lead_scores_recommendation"),
        ),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["campaigns.id"],
            name=op.f("fk_lead_scores_campaign_id_campaigns"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name=op.f("fk_lead_scores_lead_id_leads"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_run_id"],
            ["task_runs.id"],
            name=op.f("fk_lead_scores_task_run_id_task_runs"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead_scores")),
    )
    op.create_index(
        op.f("ix_lead_scores_campaign_id"),
        "lead_scores",
        ["campaign_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lead_scores_lead_id"),
        "lead_scores",
        ["lead_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lead_scores_recommendation"),
        "lead_scores",
        ["recommendation"],
        unique=False,
    )
    op.create_index(
        op.f("ix_lead_scores_task_run_id"),
        "lead_scores",
        ["task_run_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_lead_scores_task_run_id"), table_name="lead_scores")
    op.drop_index(op.f("ix_lead_scores_recommendation"), table_name="lead_scores")
    op.drop_index(op.f("ix_lead_scores_lead_id"), table_name="lead_scores")
    op.drop_index(op.f("ix_lead_scores_campaign_id"), table_name="lead_scores")
    op.drop_table("lead_scores")

    op.execute("DELETE FROM task_runs WHERE task_type = 'lead_scoring'")
    op.drop_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_task_runs_task_type"),
        "task_runs",
        "task_type IN ('lead_discovery', 'lead_validation')",
    )
