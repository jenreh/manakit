"""add_pkce_code_verifier_to_oauth_state

Revision ID: 9a8b7c6d5e4f
Revises: 4149573f35c1
Create Date: 2025-08-24 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9a8b7c6d5e4f"
down_revision: str | None = "4149573f35c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "auth_oauth_states",
        sa.Column("code_verifier", sa.String(length=200), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("auth_oauth_states", "code_verifier")
