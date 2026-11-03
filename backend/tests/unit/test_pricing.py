from decimal import Decimal

import pytest

from app.modules.orders.domain.pricing import PricingEngine


def test_weight_rounding_dec_01():
    """Verify DEC-01: Rounding to 0.1 kg using ROUND_HALF_UP."""
    assert PricingEngine.round_weight(Decimal("3.25")) == Decimal("3.3")
    assert PricingEngine.round_weight(Decimal("3.24")) == Decimal("3.2")
    assert PricingEngine.round_weight(Decimal("1.05")) == Decimal("1.1")
    assert PricingEngine.round_weight(Decimal("2.00")) == Decimal("2.0")
    assert PricingEngine.round_weight(Decimal("0.05")) == Decimal("0.1")


def test_minimum_weight_kiloan_dec_02():
    """Verify DEC-02: Minimum 3.0 kg per kiloan service item."""
    # Under minimum weight: 2.4 kg should be charged as 3.0 kg
    res_under = PricingEngine.calculate_line_item(
        pricing_type="PER_KG",
        quantity=Decimal("2.4"),
        unit_price=10000,
    )
    assert res_under.measured_quantity == Decimal("2.4")
    assert res_under.billable_quantity == Decimal("3.0")
    assert res_under.line_total == 30000

    # Under minimum weight with rounding: 2.94 kg -> 2.9 kg -> charged as 3.0 kg
    res_round_under = PricingEngine.calculate_line_item(
        pricing_type="PER_KG",
        quantity=Decimal("2.94"),
        unit_price=10000,
    )
    assert res_round_under.billable_quantity == Decimal("3.0")
    assert res_round_under.line_total == 30000

    # Above minimum weight: 4.25 kg -> 4.3 kg -> charged as 4.3 kg
    res_above = PricingEngine.calculate_line_item(
        pricing_type="PER_KG",
        quantity=Decimal("4.25"),
        unit_price=10000,
    )
    assert res_above.billable_quantity == Decimal("4.3")
    assert res_above.line_total == 43000


def test_per_item_pricing():
    """Verify per item pricing calculation and integer quantity enforcement."""
    res = PricingEngine.calculate_line_item(
        pricing_type="PER_ITEM",
        quantity=Decimal("5"),
        unit_price=15000,
    )
    assert res.measured_quantity == Decimal("5")
    assert res.billable_quantity == Decimal("5")
    assert res.line_total == 75000

    # Reject non-integer quantity for per-item
    with pytest.raises(ValueError, match="harus berupa bilangan bulat"):
        PricingEngine.calculate_line_item(
            pricing_type="PER_ITEM",
            quantity=Decimal("2.5"),
            unit_price=15000,
        )


def test_order_total_calculation():
    """Verify order calculation with multiple items, extra charge, and delivery fee."""
    items = [
        ("PER_KG", Decimal("2.0"), 10000),  # billed as 3.0 kg -> 30,000
        ("PER_ITEM", Decimal("2"), 25000),  # 2 * 25,000 = 50,000
    ]
    res = PricingEngine.calculate_order(
        items=items,
        extra_charge_amount=5000,
        delivery_fee_amount=10000,
    )

    assert res.subtotal_amount == 80000
    assert res.extra_charge_amount == 5000
    assert res.delivery_fee_amount == 10000
    assert res.total_amount == 95000
