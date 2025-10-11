"""server_version

Revision ID: 5beb0946474a
Revises: 99a9644dc419
Create Date: 2025-02-12 19:09:47.412245

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5beb0946474a"
down_revision: str | None = "99a9644dc419"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


"""Add version_gte_1_5 column to server table

Revision ID: 20231018_add_version_gte_1_5
Revises: <previous_revision_id>
Create Date: 2023-10-18 00:00:00.000000

"""

# revision identifiers, used by Alembic.
revision = "5beb0946474a"
down_revision = "99a9644dc419"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "server",
        sa.Column(
            "version_gte_1_5", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )


def downgrade() -> None:
    op.add_column("server", sa.Column("server_version", sa.String(), nullable=True))
