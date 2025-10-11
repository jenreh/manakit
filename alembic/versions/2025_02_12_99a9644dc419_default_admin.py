"""empty message

Revision ID: 99a9644dc419
Revises: e28d60677b52
Create Date: 2025-02-12 15:46:33.407885

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "99a9644dc419"
down_revision: str | None = "e28d60677b52"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO public.oauth_user
        (id, email, firstname, lastname, is_active, is_superuser, is_verified, hashed_password, created_at, updated_at)
        VALUES(
            'a9c26f2f-6c9a-4361-bc0a-cdf6e9dff4db'::uuid,
            'admin@aila-solutions.com',
            'Admin',
            'Account',
            true,
            true,
            true,
            '$argon2id$v=19$m=65536,t=3,p=4$SgnyFbZZERtpb1Yg6rqoFw$yhM9+KKparabGwpXuGzvbJt3xCTVOcKVPaoc8p3cAxk',
            '2025-02-03 10:18:40.258',
            '2025-02-03 10:19:14.354'
        );
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM public.oauth_user WHERE id = 'a9c26f2f-6c9a-4361-bc0a-cdf6e9dff4db';"
    )
