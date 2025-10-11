"""add_mcp_servers

Revision ID: 2025_08_01_151032_add_mcp_servers
Revises: 9beec6124919
Create Date: 2025-08-01 15:10:32.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "abc123def456"
down_revision: str | None = "9beec6124919"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create MCP servers table."""
    op.create_table(
        "mcp_server",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("headers", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_mcp_server_id"), "mcp_server", ["id"], unique=False)


def downgrade() -> None:
    """Drop MCP servers table."""
    op.drop_index(op.f("ix_mcp_server_id"), table_name="mcp_server")
    op.drop_table("mcp_server")
