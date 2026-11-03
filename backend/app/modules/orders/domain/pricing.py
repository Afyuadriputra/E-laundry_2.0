from decimal import ROUND_HALF_UP, Decimal
from typing import NamedTuple

# Decimal quantizer for 0.1 kg rounding (DEC-01)
TENTH_KG = Decimal("0.1")
MINIMUM_KILOAN_WEIGHT = Decimal("3.0")


class LinePriceResult(NamedTuple):
    measured_quantity: Decimal
    billable_quantity: Decimal
    unit_price: int
    line_total: int


class OrderPriceResult(NamedTuple):
    line_results: list[LinePriceResult]
    subtotal_amount: int
    extra_charge_amount: int
    delivery_fee_amount: int
    total_amount: int


class PricingEngine:
    @staticmethod
    def round_weight(weight: Decimal) -> Decimal:
        """Enforces DEC-01: Round weight to nearest 0.1 kg using ROUND_HALF_UP.

        Examples:
            3.25 -> 3.3
            3.24 -> 3.2
            1.05 -> 1.1
            2.00 -> 2.0
        """
        return weight.quantize(TENTH_KG, rounding=ROUND_HALF_UP)

    @classmethod
    def calculate_line_item(
        cls,
        pricing_type: str,
        quantity: Decimal,
        unit_price: int,
    ) -> LinePriceResult:
        """Calculate line item price based on pricing type and rules."""
        if quantity <= Decimal(0):
            raise ValueError("Kuantitas pesanan harus lebih besar dari 0.")
        if unit_price < 0:
            raise ValueError("Harga satuan tidak boleh negatif.")

        if pricing_type == "PER_KG":
            rounded_weight = cls.round_weight(quantity)
            # Enforce DEC-02: minimum 3.0 kg billable floor
            billable_weight = max(rounded_weight, MINIMUM_KILOAN_WEIGHT)
            line_total = int(
                (billable_weight * Decimal(unit_price)).to_integral_value(ROUND_HALF_UP)
            )
            return LinePriceResult(
                measured_quantity=quantity,
                billable_quantity=billable_weight,
                unit_price=unit_price,
                line_total=line_total,
            )
        elif pricing_type == "PER_ITEM":
            # For per-item, quantity must be a whole positive integer
            if quantity != quantity.to_integral_value():
                raise ValueError("Kuantitas layanan per satuan (pcs) harus berupa bilangan bulat.")
            billable_qty = quantity
            line_total = int(quantity * unit_price)
            return LinePriceResult(
                measured_quantity=quantity,
                billable_quantity=billable_qty,
                unit_price=unit_price,
                line_total=line_total,
            )
        else:
            raise ValueError(f"Metode penentuan harga '{pricing_type}' tidak dikenali.")

    @classmethod
    def calculate_order(
        cls,
        items: list[tuple[str, Decimal, int]],  # [(pricing_type, quantity, unit_price)]
        extra_charge_amount: int = 0,
        delivery_fee_amount: int = 0,
    ) -> OrderPriceResult:
        if not items:
            raise ValueError("Pesanan harus memiliki minimal satu item layanan.")
        if extra_charge_amount < 0:
            raise ValueError("Biaya tambahan (extra charge) tidak boleh negatif.")
        if delivery_fee_amount < 0:
            raise ValueError("Biaya antar/jemput (delivery fee) tidak boleh negatif.")

        line_results: list[LinePriceResult] = []
        subtotal = 0

        for pricing_type, quantity, unit_price in items:
            res = cls.calculate_line_item(pricing_type, quantity, unit_price)
            line_results.append(res)
            subtotal += res.line_total

        total = subtotal + extra_charge_amount + delivery_fee_amount

        return OrderPriceResult(
            line_results=line_results,
            subtotal_amount=subtotal,
            extra_charge_amount=extra_charge_amount,
            delivery_fee_amount=delivery_fee_amount,
            total_amount=total,
        )
