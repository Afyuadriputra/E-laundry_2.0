import pytest

from app.core.exceptions import BusinessInvariantException
from app.modules.orders.domain.state_machine import OperationalStatus, OrderStateMachine


def test_standard_forward_workflow():
    """Verify standard progression: RECEIVED to READY."""
    assert OrderStateMachine.can_transition(OperationalStatus.RECEIVED, OperationalStatus.QUEUED)
    assert OrderStateMachine.can_transition(OperationalStatus.QUEUED, OperationalStatus.WASHING)
    assert OrderStateMachine.can_transition(OperationalStatus.WASHING, OperationalStatus.DRYING)
    assert OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.IRONING, requires_ironing=True
    )
    assert OrderStateMachine.can_transition(OperationalStatus.IRONING, OperationalStatus.QC_PACKING)
    assert OrderStateMachine.can_transition(OperationalStatus.QC_PACKING, OperationalStatus.READY)


def test_skip_ironing_when_not_required():
    """Verify DRYING -> QC_PACKING skip when service doesn't require ironing."""
    # When service does not require ironing, DRYING -> QC_PACKING is valid
    assert OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.QC_PACKING, requires_ironing=False
    )

    # When service does not require ironing, transitioning to IRONING is rejected
    assert not OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.IRONING, requires_ironing=False
    )


def test_invalid_transition_skips():
    """Verify invalid skipped states are rejected."""
    # Cannot jump directly from RECEIVED to READY
    assert not OrderStateMachine.can_transition(OperationalStatus.RECEIVED, OperationalStatus.READY)
    # Cannot jump from QUEUED to COMPLETED
    assert not OrderStateMachine.can_transition(
        OperationalStatus.QUEUED, OperationalStatus.COMPLETED
    )
    # Cannot jump backwards from READY to WASHING
    assert not OrderStateMachine.can_transition(OperationalStatus.READY, OperationalStatus.WASHING)


def test_terminal_states_immutable():
    """Verify terminal states (COMPLETED, CANCELLED) cannot transition anywhere."""
    assert not OrderStateMachine.can_transition(
        OperationalStatus.COMPLETED, OperationalStatus.WASHING
    )
    assert not OrderStateMachine.can_transition(
        OperationalStatus.CANCELLED, OperationalStatus.WASHING
    )
    assert not OrderStateMachine.can_transition(
        OperationalStatus.CANCELLED, OperationalStatus.RECEIVED
    )

    with pytest.raises(BusinessInvariantException, match="berstatus terminal"):
        OrderStateMachine.validate_transition(
            from_status=OperationalStatus.CANCELLED,
            to_status=OperationalStatus.WASHING,
        )


def test_cancellation_requires_reason():
    """Verify cancellation from active state requires cancellation reason."""
    # Cancellation allowed with reason
    OrderStateMachine.validate_transition(
        from_status=OperationalStatus.WASHING,
        to_status=OperationalStatus.CANCELLED,
        cancellation_reason="Pelanggan membatalkan pesanan",
    )

    # Rejection if reason is empty or None
    with pytest.raises(BusinessInvariantException, match="memerlukan alasan pembatalan"):
        OrderStateMachine.validate_transition(
            from_status=OperationalStatus.WASHING,
            to_status=OperationalStatus.CANCELLED,
            cancellation_reason=None,
        )


def test_order_completion_staged_negative_validation():
    """Verify M2 invariant: READY -> COMPLETED rejected without handoff and payment."""
    # Rejection when handoff missing
    with pytest.raises(BusinessInvariantException, match="tanpa bukti fisik serah terima"):
        OrderStateMachine.validate_transition(
            from_status=OperationalStatus.READY,
            to_status=OperationalStatus.COMPLETED,
            has_handoff=False,
            is_fully_paid=True,
        )

    # Rejection when unpaid
    with pytest.raises(BusinessInvariantException, match="karena tagihan belum lunas"):
        OrderStateMachine.validate_transition(
            from_status=OperationalStatus.READY,
            to_status=OperationalStatus.COMPLETED,
            has_handoff=True,
            is_fully_paid=False,
        )

    # Acceptance only when both conditions are satisfied
    OrderStateMachine.validate_transition(
        from_status=OperationalStatus.READY,
        to_status=OperationalStatus.COMPLETED,
        has_handoff=True,
        is_fully_paid=True,
    )
