"""Create initial tables for project references

Revision ID: 1a2b3c4d5e6f
Revises: 5beb0946474a
Create Date: 2023-05-01

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "1a2b3c4d5e6f"
down_revision = "5beb0946474a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create enum types
    ciu_enum = sa.Enum("CP", "H", "IMC", "M", "MCI", "P", "TT", "U", name="ciuenum")
    ciu_enum.create(op.get_bind())

    proficiency_enum = sa.Enum(
        "MT", "A1", "A2", "B1", "B2", "C1", "C2", name="proficiency"
    )
    proficiency_enum.create(op.get_bind())

    # Create tables
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(50), nullable=False, index=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "technology",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(50), nullable=False, index=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "profile",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(100), nullable=False, index=True),
        sa.Column("last_name", sa.String(100), nullable=False, index=True),
        sa.Column("position", sa.String(100), nullable=False, server_default=""),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "projectreference",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("ciu", sa.String(3), nullable=False),
        sa.Column("name", sa.String(100), nullable=False, index=True),
        sa.Column("customer", sa.String(100), nullable=False, index=True),
        sa.Column(
            "customer_contact", sa.String(100), nullable=False, server_default=""
        ),
        sa.Column("started", sa.Date(), nullable=False),
        sa.Column("ended", sa.Date(), nullable=True),
        sa.Column("summary", sa.String(2000), nullable=False, server_default=""),
        sa.Column("description", sa.String(25000), nullable=False, server_default=""),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "workexperience",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("company", sa.String(100), nullable=False, index=True),
        sa.Column("position", sa.String(100), nullable=False, server_default=""),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.String(5000), nullable=False, server_default=""),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("institution", sa.String(100), nullable=False, index=True),
        sa.Column("degree", sa.String(100), nullable=False, server_default=""),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.String(5000), nullable=False, server_default=""),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "language",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(100), nullable=False, index=True),
        sa.Column("proficiency", sa.String(2), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create association tables
    op.create_table(
        "referencetaglink",
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["reference_id"], ["projectreference.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tag.id"]),
        sa.PrimaryKeyConstraint("reference_id", "tag_id"),
    )

    op.create_table(
        "referencetechnologylink",
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("technology_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["reference_id"], ["projectreference.id"]),
        sa.ForeignKeyConstraint(["technology_id"], ["technology.id"]),
        sa.PrimaryKeyConstraint("reference_id", "technology_id"),
    )

    op.create_table(
        "referenceteammemberlink",
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(100), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(["reference_id"], ["projectreference.id"]),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"]),
        sa.PrimaryKeyConstraint("reference_id", "profile_id"),
    )


def downgrade() -> None:
    # Drop tables in reverse order to avoid foreign key constraint violations
    op.drop_table("referenceteammemberlink")
    op.drop_table("referencetechnologylink")
    op.drop_table("referencetaglink")
    op.drop_table("language")
    op.drop_table("education")
    op.drop_table("workexperience")
    op.drop_table("projectreference")
    op.drop_table("profile")
    op.drop_table("technology")
    op.drop_table("tag")

    # Drop enums
    sa.Enum(name="proficiency").drop(op.get_bind())
    sa.Enum(name="ciuenum").drop(op.get_bind())
