"""m3_finance_and_digital_invoices

Revision ID: d912a784c4e1
Revises: 7a89e41b2c10
Create Date: 2026-11-03 15:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd912a784c4e1'
down_revision: str | None = '7a89e41b2c10'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('order_id', sa.Uuid(), nullable=False),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('method', sa.String(length=30), nullable=False),
        sa.Column(
            'verification_status',
            sa.String(length=20),
            server_default='VERIFIED',
            nullable=False,
        ),
        sa.Column(
            'payment_time',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('verified_by', sa.Uuid(), nullable=False),
        sa.Column(
            'verified_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('reference_note', sa.String(length=255), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint('amount > 0', name='chk_payments_amount_positive'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_payments_order_id', 'payments', ['order_id'], unique=False)
    op.create_index(
        'idx_payments_order_time',
        'payments',
        ['order_id', 'payment_time'],
        unique=False,
    )

    # 2. Create payment_voids table
    op.create_table(
        'payment_voids',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('payment_id', sa.Uuid(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('voided_by', sa.Uuid(), nullable=False),
        sa.Column(
            'voided_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['voided_by'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('payment_id', name='uq_payment_voids_payment_id'),
    )
    op.create_index('ix_payment_voids_payment_id', 'payment_voids', ['payment_id'], unique=True)

    # 3. Create expenses table
    op.create_table(
        'expenses',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('business_id', sa.Uuid(), nullable=False),
        sa.Column('category', sa.String(length=60), nullable=False),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('expense_date', sa.Date(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Uuid(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint('amount > 0', name='chk_expenses_amount_positive'),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_expenses_business_id', 'expenses', ['business_id'], unique=False)
    op.create_index(
        'idx_expenses_business_date',
        'expenses',
        ['business_id', 'expense_date'],
        unique=False,
    )

    # 4. Create idempotency_records table
    op.create_table(
        'idempotency_records',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('scope_key', sa.String(length=150), nullable=False),
        sa.Column('operation', sa.String(length=100), nullable=False),
        sa.Column('idempotency_key_hash', sa.String(length=128), nullable=False),
        sa.Column('request_hash', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('response_status_code', sa.Integer(), nullable=True),
        sa.Column('response_reference', sa.Text(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'scope_key',
            'operation',
            'idempotency_key_hash',
            name='uq_idempotency_scope_op_key',
        ),
    )


def downgrade() -> None:
    op.drop_table('idempotency_records')
    op.drop_index('idx_expenses_business_date', table_name='expenses')
    op.drop_index('ix_expenses_business_id', table_name='expenses')
    op.drop_table('expenses')
    op.drop_index('ix_payment_voids_payment_id', table_name='payment_voids')
    op.drop_table('payment_voids')
    op.drop_index('idx_payments_order_time', table_name='payments')
    op.drop_index('ix_payments_order_id', table_name='payments')
    op.drop_table('payments')
