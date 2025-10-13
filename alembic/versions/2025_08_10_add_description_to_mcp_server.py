"""add_description_to_mcp_server

Revision ID: d7a1c2b3e4f5
Revises: abc123def456
Create Date: 2025-08-10 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7a1c2b3e4f5"
down_revision: str | None = "abc123def456"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add description column to mcp_server table."""
    op.add_column(
        "mcp_server",
        sa.Column("description", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Remove description column from mcp_server table."""
    op.drop_column("mcp_server", "description")
