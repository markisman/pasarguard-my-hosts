"""add admin_host_overrides (feature: My Hosts)

Revision ID: mh0st0v3r1ds
Revises: <PUT_CURRENT_HEAD_HERE>
Create Date: 2026-10-15

NOTE: set `down_revision` to the current head. Find it with:
    docker exec pasarguard-pasarguard-1 alembic heads
or
    ls app/db/migrations/versions | tail
"""
import sqlalchemy as sa
from alembic import op

revision = "mh0st0v3r1ds"
down_revision = "PUT_CURRENT_HEAD_HERE"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin_host_overrides",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("admin_id", sa.BigInteger(), sa.ForeignKey("admins.id", ondelete="CASCADE"), nullable=False),
        sa.Column("host_id", sa.BigInteger(), sa.ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_name", sa.String(256), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=True),
        sa.Column("is_disabled", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.UniqueConstraint("admin_id", "host_id", name="uix_admin_host_override"),
    )
    op.create_index("ix_admin_host_overrides_admin_id", "admin_host_overrides", ["admin_id"])
    op.create_index("ix_admin_host_overrides_host_id", "admin_host_overrides", ["host_id"])


def downgrade() -> None:
    op.drop_index("ix_admin_host_overrides_host_id", table_name="admin_host_overrides")
    op.drop_index("ix_admin_host_overrides_admin_id", table_name="admin_host_overrides")
    op.drop_table("admin_host_overrides")
