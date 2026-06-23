"""Create company_profiles baseline table."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260622_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "company_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("owner_id", sa.String(length=36), nullable=True),
        sa.Column("workspace_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("industry", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_market", sa.String(length=255), nullable=True),
        sa.Column("value_proposition", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_company_profiles")),
    )
    op.create_index(
        op.f("ix_company_profiles_owner_id"),
        "company_profiles",
        ["owner_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_company_profiles_workspace_id"),
        "company_profiles",
        ["workspace_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_company_profiles_workspace_id"), table_name="company_profiles")
    op.drop_index(op.f("ix_company_profiles_owner_id"), table_name="company_profiles")
    op.drop_table("company_profiles")
