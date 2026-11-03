"""m5_pickup_and_delivery_logistics

Revision ID: e528b96f140a
Revises: c018a74e512b
Create Date: 2026-11-03 18:57:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e528b96f140a"
down_revision: str | None = "c018a74e512b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create pickup_requests table (BSD.md §20)
    op.create_table(
        "pickup_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("request_number", sa.String(length=40), nullable=False),
        sa.Column("requester_name", sa.String(length=150), nullable=False),
        sa.Column("phone_e164", sa.String(length=20), nullable=False),
        sa.Column("pickup_address", sa.Text(), nullable=False),
        sa.Column("requested_date", sa.Date(), nullable=False),
        sa.Column("requested_time_start", sa.Time(), nullable=False),
        sa.Column("requested_time_end", sa.Time(), nullable=False),
        sa.Column("confirmed_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("confirmed_end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=30), server_default="REQUESTED", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_number"),
    )
    op.create_index(
        "ix_pickup_requests_business_status",
        "pickup_requests",
        ["business_id", "status"],
    )
    op.create_index(
        "ix_pickup_requests_requested_date",
        "pickup_requests",
        ["requested_date"],
    )
    op.create_index(
        "ix_pickup_requests_request_number",
        "pickup_requests",
        ["request_number"],
        unique=True,
    )

    # 2. Create delivery_tasks table (BSD.md §21)
    op.create_table(
        "delivery_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_type", sa.String(length=20), nullable=False),
        sa.Column("pickup_request_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("courier_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("scheduled_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=30), server_default="PENDING", nullable=False),
        sa.Column("recipient_name", sa.String(length=150), nullable=True),
        sa.Column("destination_address", sa.Text(), nullable=False),
        sa.Column("destination_phone", sa.String(length=20), nullable=True),
        sa.Column("proof_photo_path", sa.Text(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(task_type = 'PICKUP' AND pickup_request_id IS NOT NULL AND order_id IS NULL) OR "
            "(task_type = 'DELIVERY' AND order_id IS NOT NULL AND pickup_request_id IS NULL)",
            name="chk_delivery_tasks_type_target",
        ),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["courier_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["pickup_request_id"], ["pickup_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_delivery_tasks_courier_status",
        "delivery_tasks",
        ["courier_user_id", "status"],
    )
    op.create_index(
        "ix_delivery_tasks_pickup_request_id",
        "delivery_tasks",
        ["pickup_request_id"],
    )
    op.create_index(
        "ix_delivery_tasks_order_id",
        "delivery_tasks",
        ["order_id"],
    )

    # 3. Create delivery_status_history table (BSD.md §22)
    op.create_table(
        "delivery_status_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("delivery_task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("from_status", sa.String(length=30), nullable=True),
        sa.Column("to_status", sa.String(length=30), nullable=False),
        sa.Column("changed_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["changed_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["delivery_task_id"], ["delivery_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_delivery_status_history_task_id",
        "delivery_status_history",
        ["delivery_task_id", "created_at"],
    )

    # 4. Resolve Deferred Cross-Milestone Foreign Keys
    op.create_foreign_key(
        "fk_orders_pickup_request_id",
        "orders",
        "pickup_requests",
        ["pickup_request_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_tracking_tokens_pickup_request_id",
        "tracking_tokens",
        "pickup_requests",
        ["pickup_request_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_order_handoffs_delivery_task_id",
        "order_handoffs",
        "delivery_tasks",
        ["delivery_task_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    # 1. Drop Deferred Foreign Keys
    op.drop_constraint("fk_order_handoffs_delivery_task_id", "order_handoffs", type_="foreignkey")
    op.drop_constraint("fk_tracking_tokens_pickup_request_id", "tracking_tokens", type_="foreignkey")
    op.drop_constraint("fk_orders_pickup_request_id", "orders", type_="foreignkey")

    # 2. Drop Tables
    op.drop_table("delivery_status_history")
    op.drop_table("delivery_tasks")
    op.drop_table("pickup_requests")
