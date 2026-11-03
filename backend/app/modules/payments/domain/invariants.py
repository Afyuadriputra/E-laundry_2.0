from app.core.exceptions import AppException


class PaymentDomainException(AppException):
    """Base exception for payment domain errors."""

    def __init__(self, code: str, message: str, status_code: int = 422):
        super().__init__(
            code=code,
            message=message,
            status_code=status_code,
        )


class AmountMustBePositiveError(PaymentDomainException):
    def __init__(self, amount: int):
        super().__init__(
            code="PAYMENT_AMOUNT_INVALID",
            message=f"Nominal pembayaran harus lebih besar dari 0. Diterima: Rp {amount:,}.",
        )


class OverpaymentNotAllowedError(PaymentDomainException):
    def __init__(self, amount: int, remaining: int):
        super().__init__(
            code="OVERPAYMENT_NOT_ALLOWED",
            message=(
                f"Nominal pembayaran (Rp {amount:,}) melebihi sisa tagihan pesanan "
                f"(Rp {remaining:,}). Overpayment tidak diizinkan."
            ),
        )


class OrderCancelledPaymentError(PaymentDomainException):
    def __init__(self, order_number: str):
        super().__init__(
            code="ORDER_CANCELLED_PAYMENT",
            message=(
                f"Tidak dapat menerima pembayaran untuk pesanan yang telah dibatalkan ({order_number})."
            ),
        )


class PaymentAlreadyVoidedError(PaymentDomainException):
    def __init__(self, payment_id: str):
        super().__init__(
            code="PAYMENT_ALREADY_VOIDED",
            message=f"Pembayaran {payment_id} telah dibatalkan sebelumnya dan tidak dapat di-void ulang.",
            status_code=409,
        )


class VoidReasonRequiredError(PaymentDomainException):
    def __init__(self):
        super().__init__(
            code="VOID_REASON_REQUIRED",
            message="Alasan pembatalan (void) pembayaran wajib diisi.",
        )
