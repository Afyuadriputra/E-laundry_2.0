import uuid
from datetime import UTC, datetime

from app.modules.payments.domain.balance import (
    PaymentStatus,
    calculate_payment_balance,
)
from app.modules.payments.models import Payment, PaymentVoid


def test_payment_balance_unpaid_when_no_payments():
    balance = calculate_payment_balance(total_amount=50000, payments=[])
    assert balance.total_amount == 50000
    assert balance.total_paid == 0
    assert balance.remaining_amount == 50000
    assert balance.payment_status == PaymentStatus.UNPAID
    assert balance.verified_payment_count == 0
    assert balance.voided_payment_count == 0


def test_payment_balance_partially_paid():
    p1 = Payment(
        id=uuid.uuid4(),
        order_id=uuid.uuid4(),
        amount=20000,
        method="CASH",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=uuid.uuid4(),
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    p1.void_record = None

    balance = calculate_payment_balance(total_amount=50000, payments=[p1])
    assert balance.total_paid == 20000
    assert balance.remaining_amount == 30000
    assert balance.payment_status == PaymentStatus.PARTIALLY_PAID
    assert balance.verified_payment_count == 1
    assert balance.voided_payment_count == 0


def test_payment_balance_fully_paid():
    p1 = Payment(
        id=uuid.uuid4(),
        order_id=uuid.uuid4(),
        amount=30000,
        method="BANK_TRANSFER",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=uuid.uuid4(),
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    p1.void_record = None

    p2 = Payment(
        id=uuid.uuid4(),
        order_id=uuid.uuid4(),
        amount=20000,
        method="QRIS_MANUAL",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=uuid.uuid4(),
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    p2.void_record = None

    balance = calculate_payment_balance(total_amount=50000, payments=[p1, p2])
    assert balance.total_paid == 50000
    assert balance.remaining_amount == 0
    assert balance.payment_status == PaymentStatus.PAID
    assert balance.verified_payment_count == 2
    assert balance.voided_payment_count == 0


def test_payment_balance_excludes_voided_payments():
    p1 = Payment(
        id=uuid.uuid4(),
        order_id=uuid.uuid4(),
        amount=30000,
        method="CASH",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=uuid.uuid4(),
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    # Simulate void record
    void = PaymentVoid(
        id=uuid.uuid4(),
        payment_id=p1.id,
        reason="Salah input kasir",
        voided_by=uuid.uuid4(),
        voided_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    p1.void_record = void

    p2 = Payment(
        id=uuid.uuid4(),
        order_id=uuid.uuid4(),
        amount=15000,
        method="CASH",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=uuid.uuid4(),
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    p2.void_record = None

    balance = calculate_payment_balance(total_amount=50000, payments=[p1, p2])
    assert balance.total_paid == 15000  # 30000 voided is excluded
    assert balance.remaining_amount == 35000
    assert balance.payment_status == PaymentStatus.PARTIALLY_PAID
    assert balance.verified_payment_count == 1
    assert balance.voided_payment_count == 1
