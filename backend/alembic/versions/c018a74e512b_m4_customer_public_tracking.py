"""m4_customer_public_tracking

Revision ID: c018a74e512b
Revises: d912a784c4e1
Create Date: 2026-11-03 15:30:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c018a74e512b"
down_revision: str | None = "d912a784c4e1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 0. Allow changed_by in order_status_history to be nullable (customer self-cancellation via public tracking)
    op.alter_column("order_status_history", "changed_by", nullable=True)

    # 1. Create tracking_tokens table (BSD.md §23)
    op.create_table(
        "tracking_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("pickup_request_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint(
            "num_nonnulls(order_id, pickup_request_id) = 1",
            name="chk_tracking_tokens_single_target",
        ),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_tracking_tokens_token_hash",
        "tracking_tokens",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_tracking_tokens_order_id",
        "tracking_tokens",
        ["order_id"],
        unique=False,
    )
    op.create_index(
        "ix_tracking_tokens_pickup_request_id",
        "tracking_tokens",
        ["pickup_request_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_tracking_tokens_pickup_request_id", table_name="tracking_tokens")
    op.drop_index("ix_tracking_tokens_order_id", table_name="tracking_tokens")
    op.drop_index("ix_tracking_tokens_token_hash", table_name="tracking_tokens")
    op.drop_table("tracking_tokens")
