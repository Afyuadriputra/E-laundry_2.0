"""
Unit test suite for OrderStateMachine domain logic.
Tests transition matrix, branch conditions (ironing skip), terminal states,
cancellation reason invariants, and completion prerequisites.
"""

import pytest

from app.core.exceptions import BusinessInvariantException
from app.modules.orders.domain.state_machine import (
    STANDARD_TRANSITIONS,
    OperationalStatus,
    OrderStateMachine,
)


def test_status_enum_values():
    """Verify all 9 canonical operational statuses are present."""
    expected = {
        "RECEIVED",
        "QUEUED",
        "WASHING",
        "DRYING",
        "IRONING",
        "QC_PACKING",
        "READY",
        "COMPLETED",
        "CANCELLED",
    }
    actual = {s.value for s in OperationalStatus}
    assert actual == expected


def test_is_terminal_logic():
    """Verify only COMPLETED and CANCELLED are recognized as terminal."""
    assert OrderStateMachine.is_terminal(OperationalStatus.COMPLETED)
    assert OrderStateMachine.is_terminal(OperationalStatus.CANCELLED)
    for status in OperationalStatus:
        if status not in (OperationalStatus.COMPLETED, OperationalStatus.CANCELLED):
            assert not OrderStateMachine.is_terminal(status)


def test_exhaustive_non_allowed_transitions():
    """Verify transitions outside the canonical workflow are rejected."""
    for from_status in OperationalStatus:
        for to_status in OperationalStatus:
            if to_status == OperationalStatus.CANCELLED and not OrderStateMachine.is_terminal(from_status):
                continue
            allowed = STANDARD_TRANSITIONS.get(from_status.value, set())
            if to_status.value not in allowed:
                assert not OrderStateMachine.can_transition(from_status, to_status)
                with pytest.raises(BusinessInvariantException):
                    OrderStateMachine.validate_transition(from_status, to_status)


def test_ironing_branch_matrix():
    """Verify conditional transitions for drying with/without ironing requirement."""
    # When ironing is needed: DRYING -> IRONING is valid, DRYING -> QC_PACKING is valid in standard set but can_transition checks
    assert OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.IRONING, requires_ironing=True
    )
    assert OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.QC_PACKING, requires_ironing=True
    )

    # When ironing is NOT needed: DRYING -> QC_PACKING is allowed, DRYING -> IRONING is forbidden
    assert OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.QC_PACKING, requires_ironing=False
    )
    assert not OrderStateMachine.can_transition(
        OperationalStatus.DRYING, OperationalStatus.IRONING, requires_ironing=False
    )


def test_cancellation_from_all_active_states():
    """Verify any active status can transition to CANCELLED with valid reason."""
    active_statuses = [
        OperationalStatus.RECEIVED,
        OperationalStatus.QUEUED,
        OperationalStatus.WASHING,
        OperationalStatus.DRYING,
        OperationalStatus.IRONING,
        OperationalStatus.QC_PACKING,
        OperationalStatus.READY,
    ]
    for status in active_statuses:
        assert OrderStateMachine.can_transition(status, OperationalStatus.CANCELLED)
        # Should not raise exception
        OrderStateMachine.validate_transition(
            status,
            OperationalStatus.CANCELLED,
            cancellation_reason="Batal oleh kasir atas permintaan pelanggan",
        )

        # Empty reason should raise
        with pytest.raises(BusinessInvariantException, match="alasan pembatalan"):
            OrderStateMachine.validate_transition(
                status,
                OperationalStatus.CANCELLED,
                cancellation_reason="   ",
            )


def test_completion_staged_invariants():
    """Verify READY -> COMPLETED strictly requires both handoff and full payment."""
    # Both missing
    with pytest.raises(BusinessInvariantException, match="tanpa bukti fisik serah terima"):
        OrderStateMachine.validate_transition(
            OperationalStatus.READY,
            OperationalStatus.COMPLETED,
            has_handoff=False,
            is_fully_paid=False,
        )

    # Handoff present, unpaid
    with pytest.raises(BusinessInvariantException, match="karena tagihan belum lunas"):
        OrderStateMachine.validate_transition(
            OperationalStatus.READY,
            OperationalStatus.COMPLETED,
            has_handoff=True,
            is_fully_paid=False,
        )

    # Paid, handoff missing
    with pytest.raises(BusinessInvariantException, match="tanpa bukti fisik serah terima"):
        OrderStateMachine.validate_transition(
            OperationalStatus.READY,
            OperationalStatus.COMPLETED,
            has_handoff=False,
            is_fully_paid=True,
        )

    # Both satisfied -> Success
    OrderStateMachine.validate_transition(
        OperationalStatus.READY,
        OperationalStatus.COMPLETED,
        has_handoff=True,
        is_fully_paid=True,
    )

