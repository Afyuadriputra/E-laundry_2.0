"""m2_core_laundry_operations

Revision ID: 7a89e41b2c10
Revises: ec501d8d2522
Create Date: 2026-11-03 14:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7a89e41b2c10"
down_revision: str | Sequence[str] | None = "ec501d8d2522"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema for M2: customers, services, orders, order items, and handoffs."""
    # 1. customers table
    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("phone_e164", sa.String(length=20), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_customers_business_id", "customers", ["business_id"])
    op.create_index("ix_customers_full_name", "customers", ["full_name"])
    op.create_index("ix_customers_phone_e164", "customers", ["phone_e164"])
    op.create_index("ix_customers_business_name", "customers", ["business_id", "full_name"])
    op.create_index("ix_customers_business_phone", "customers", ["business_id", "phone_e164"])

    # 2. services table
    op.create_table(
        "services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("pricing_type", sa.String(length=20), nullable=False),
        sa.Column("unit", sa.String(length=20), nullable=False),
        sa.Column("unit_price", sa.BigInteger(), nullable=False),
        sa.Column("estimated_hours", sa.Integer(), nullable=True),
        sa.Column(
            "requires_ironing", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.CheckConstraint("unit_price >= 0", name="ck_services_unit_price"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_services_business_id", "services", ["business_id"])
    op.create_index("ix_services_business_name", "services", ["business_id", "name"])
    op.create_index("ix_services_business_active", "services", ["business_id", "is_active"])

    # 3. orders table (pickup_request_id is plain nullable UUID, FK deferred to M5)
    op.create_table(
        "orders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("order_number", sa.String(length=40), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("pickup_request_id", sa.Uuid(), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column(
            "operational_status", sa.String(length=30), nullable=False, server_default="RECEIVED"
        ),
        sa.Column("intake_method", sa.String(length=30), nullable=False),
        sa.Column("return_method", sa.String(length=30), nullable=False),
        sa.Column("subtotal_amount", sa.BigInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "extra_charge_amount", sa.BigInteger(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "delivery_fee_amount", sa.BigInteger(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column("total_amount", sa.BigInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("estimated_completion_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("customer_notes", sa.Text(), nullable=True),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
        sa.CheckConstraint("subtotal_amount >= 0", name="ck_orders_subtotal_amount"),
        sa.CheckConstraint("extra_charge_amount >= 0", name="ck_orders_extra_charge_amount"),
        sa.CheckConstraint("delivery_fee_amount >= 0", name="ck_orders_delivery_fee_amount"),
        sa.CheckConstraint("total_amount >= 0", name="ck_orders_total_amount"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_number"),
        sa.UniqueConstraint("pickup_request_id"),
    )
    op.create_index("ix_orders_order_number", "orders", ["order_number"])
    op.create_index("ix_orders_business_id", "orders", ["business_id"])
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])
    op.create_index("ix_orders_operational_status", "orders", ["operational_status"])
    op.create_index("ix_orders_business_status", "orders", ["business_id", "operational_status"])
    op.create_index("ix_orders_business_created", "orders", ["business_id", "created_at"])

    # 4. order_items table
    op.create_table(
        "order_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("service_id", sa.Uuid(), nullable=False),
        sa.Column("service_name_snapshot", sa.String(length=150), nullable=False),
        sa.Column("pricing_type_snapshot", sa.String(length=20), nullable=False),
        sa.Column("unit_snapshot", sa.String(length=20), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=10, scale=3), nullable=False),
        sa.Column("unit_price_snapshot", sa.BigInteger(), nullable=False),
        sa.Column("line_total_amount", sa.BigInteger(), nullable=False),
        sa.Column("requires_ironing_snapshot", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.CheckConstraint("quantity > 0", name="ck_order_items_quantity"),
        sa.CheckConstraint("unit_price_snapshot >= 0", name="ck_order_items_unit_price"),
        sa.CheckConstraint("line_total_amount >= 0", name="ck_order_items_line_total"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])

    # 5. order_status_history table
    op.create_table(
        "order_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("from_status", sa.String(length=30), nullable=True),
        sa.Column("to_status", sa.String(length=30), nullable=False),
        sa.Column("changed_by", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["changed_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_status_history_order_id", "order_status_history", ["order_id"])

    # 6. order_handoffs table (delivery_task_id is plain nullable UUID, FK deferred to M5)
    op.create_table(
        "order_handoffs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("delivery_task_id", sa.Uuid(), nullable=True),
        sa.Column("handoff_method", sa.String(length=30), nullable=False),
        sa.Column("received_by_name", sa.String(length=150), nullable=True),
        sa.Column("confirmed_by_user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "confirmed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["confirmed_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
    )


def downgrade() -> None:
    """Downgrade schema for M2."""
    op.drop_table("order_handoffs")
    op.drop_table("order_status_history")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("services")
    op.drop_table("customers")
