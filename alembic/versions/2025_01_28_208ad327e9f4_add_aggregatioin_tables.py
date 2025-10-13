"""add aggregatioin tables

Revision ID: 208ad327e9f4
Revises: d862b1d42d28
Create Date: 2025-01-28 21:46:13.744334

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "208ad327e9f4"
down_revision: str | None = "d862b1d42d28"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "aggregated_usage_data",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("tenant_name", sa.String(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=False),
        sa.Column("sum_api_calls", sa.Integer(), nullable=True),
        sa.Column("sum_input_tokens", sa.Integer(), nullable=True),
        sa.Column("sum_output_tokens", sa.Integer(), nullable=True),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("hour", sa.Integer(), nullable=False),
        sa.Column("server_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["server_id"], ["server.id"], name="fk_aggregated_usage_data_server_id"
        ),
    )
    op.create_index("ix_aggregated_usage_data_day", "aggregated_usage_data", ["day"])

    op.create_table(
        "aggregated_usage_data_monthly",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("tenant_name", sa.String(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=False),
        sa.Column("sum_api_calls", sa.Integer(), nullable=True),
        sa.Column("sum_input_tokens", sa.Integer(), nullable=True),
        sa.Column("sum_output_tokens", sa.Integer(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("server_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["server_id"],
            ["server.id"],
            name="fk_aggregated_usage_data_monthly_server_id",
        ),
    )
    op.create_index(
        "ix_aggregated_usage_data_monthly_year_month",
        "aggregated_usage_data_monthly",
        ["year", "month"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_aggregated_usage_data_monthly_server_id",
        "aggregated_usage_data_monthly",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_aggregated_usage_data_server_id",
        "aggregated_usage_data",
        type_="foreignkey",
    )
    op.drop_index("ix_aggregated_usage_data_monthly_year_month")
    op.drop_index("ix_aggregated_usage_data_day")
    op.drop_table("aggregated_usage_data_monthly")
    op.drop_table("aggregated_usage_data")
