"""add servers

Revision ID: d862b1d42d28
Revises:
Create Date: 2025-01-26 13:16:41.336214

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d862b1d42d28"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "server",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), unique=True),
        sa.Column("url", sa.String, unique=True),
        sa.Column("api_key", sa.String),
    )


def downgrade() -> None:
    op.drop_table("server")
