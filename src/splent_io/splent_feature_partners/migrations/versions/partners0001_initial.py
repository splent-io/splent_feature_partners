"""partner table (collaborating organisations).

Revision ID: partners0001
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "partners0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "partner",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("link", sa.String(length=512), nullable=True),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["media_id"], ["media_item.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_partner_media_id"), "partner", ["media_id"])
    op.create_index(op.f("ix_partner_order"), "partner", ["order"])
    op.create_index(op.f("ix_partner_active"), "partner", ["active"])


def downgrade():
    op.drop_index(op.f("ix_partner_active"), table_name="partner")
    op.drop_index(op.f("ix_partner_order"), table_name="partner")
    op.drop_index(op.f("ix_partner_media_id"), table_name="partner")
    op.drop_table("partner")
