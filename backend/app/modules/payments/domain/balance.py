from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from app.modules.payments.models import Payment


class PaymentStatus(StrEnum):
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"


@dataclass(frozen=True)
class PaymentBalance:
    total_amount: int
    total_paid: int
    remaining_amount: int
    payment_status: PaymentStatus
    verified_payment_count: int
    voided_payment_count: int


def calculate_payment_balance(total_amount: int, payments: Sequence[Payment]) -> PaymentBalance:
    """Derive real-time payment balance and status according to BSD.md Section 18.4.

    remaining_amount = total_amount - verified_non_voided_payments
    Status is strictly derived: UNPAID, PARTIALLY_PAID, or PAID.
    """
    verified_non_voided = [
        p for p in payments
        if p.verification_status == "VERIFIED" and not p.is_voided
    ]
    voided = [p for p in payments if p.is_voided]

    total_paid = sum(p.amount for p in verified_non_voided)
    remaining_amount = max(0, total_amount - total_paid)

    if total_amount == 0:
        status = PaymentStatus.PAID
    elif total_paid >= total_amount:
        status = PaymentStatus.PAID
    elif total_paid > 0:
        status = PaymentStatus.PARTIALLY_PAID
    else:
        status = PaymentStatus.UNPAID

    return PaymentBalance(
        total_amount=total_amount,
        total_paid=total_paid,
        remaining_amount=remaining_amount,
        payment_status=status,
        verified_payment_count=len(verified_non_voided),
        voided_payment_count=len(voided),
    )
