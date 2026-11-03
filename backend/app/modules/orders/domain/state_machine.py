from enum import StrEnum

from app.core.exceptions import BusinessInvariantException


class OperationalStatus(StrEnum):
    RECEIVED = "RECEIVED"
    QUEUED = "QUEUED"
    WASHING = "WASHING"
    DRYING = "DRYING"
    IRONING = "IRONING"
    QC_PACKING = "QC_PACKING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# Normal forward progression lookup
STANDARD_TRANSITIONS: dict[str, set[str]] = {
    OperationalStatus.RECEIVED.value: {OperationalStatus.QUEUED.value},
    OperationalStatus.QUEUED.value: {OperationalStatus.WASHING.value},
    OperationalStatus.WASHING.value: {OperationalStatus.DRYING.value},
    OperationalStatus.DRYING.value: {
        OperationalStatus.IRONING.value,
        OperationalStatus.QC_PACKING.value,
    },
    OperationalStatus.IRONING.value: {OperationalStatus.QC_PACKING.value},
    OperationalStatus.QC_PACKING.value: {OperationalStatus.READY.value},
    OperationalStatus.READY.value: {OperationalStatus.COMPLETED.value},
    OperationalStatus.COMPLETED.value: set(),
    OperationalStatus.CANCELLED.value: set(),
}


class OrderStateMachine:
    @staticmethod
    def is_terminal(status: str) -> bool:
        return status in (OperationalStatus.COMPLETED.value, OperationalStatus.CANCELLED.value)

    @classmethod
    def can_transition(
        cls,
        from_status: str,
        to_status: str,
        requires_ironing: bool = True,
    ) -> bool:
        if cls.is_terminal(from_status):
            return False

        # Any active non-terminal status can transition to CANCELLED
        if to_status == OperationalStatus.CANCELLED.value:
            return True

        allowed_targets = STANDARD_TRANSITIONS.get(from_status, set())
        if to_status not in allowed_targets:
            return False

        # If transitioning DRYING -> IRONING, but service doesn't require ironing, reject
        if (
            from_status == OperationalStatus.DRYING.value
            and to_status == OperationalStatus.IRONING.value
        ):
            if not requires_ironing:
                return False

        return True

    @classmethod
    def validate_transition(
        cls,
        from_status: str,
        to_status: str,
        requires_ironing: bool = True,
        has_handoff: bool = False,
        is_fully_paid: bool = False,
        cancellation_reason: str | None = None,
    ) -> None:
        if cls.is_terminal(from_status):
            raise BusinessInvariantException(
                f"Pesanan berstatus terminal '{from_status}' tidak dapat diubah lagi."
            )

        if to_status == OperationalStatus.CANCELLED.value:
            if not cancellation_reason or not cancellation_reason.strip():
                raise BusinessInvariantException(
                    "Pembatalan pesanan memerlukan alasan pembatalan (cancellation_reason)."
                )
            return

        if not cls.can_transition(from_status, to_status, requires_ironing=requires_ironing):
            raise BusinessInvariantException(
                f"Transisi status dari '{from_status}' ke '{to_status}' tidak diizinkan."
            )

        # Invariant checks for COMPLETED status (BSD.md §33 & DEC-05 / DEC-12)
        if to_status == OperationalStatus.COMPLETED.value:
            if not has_handoff:
                raise BusinessInvariantException(
                    "Pesanan tidak dapat diselesaikan (COMPLETED) tanpa bukti fisik "
                    "serah terima (order handoff)."
                )
            if not is_fully_paid:
                raise BusinessInvariantException(
                    "Pesanan tidak dapat diselesaikan (COMPLETED) karena tagihan belum "
                    "lunas (status harus PAID)."
                )
