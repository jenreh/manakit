"""Create user_rights table

Revision ID: 001_create_user_rights_table
Revises:
Create Date: 2025-08-11 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1ade698f1234"
down_revision: str | None = "d7a1c2b3e4f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the user_rights table."""
    op.create_table(
        "userrights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("server_id", sa.Integer(), nullable=False),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_userrights_user_id", "user_id"),
        sa.Index("ix_userrights_server_id", "server_id"),
        sa.Index("ix_userrights_tenant_id", "tenant_id"),
        sa.UniqueConstraint(
            "user_id", "server_id", "tenant_id", name="uq_user_server_tenant"
        ),
    )


def downgrade() -> None:
    """Drop the user_rights table."""
    op.drop_table("userrights")
