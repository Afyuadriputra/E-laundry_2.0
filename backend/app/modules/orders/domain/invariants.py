import re
from datetime import UTC, datetime

from app.core.exceptions import BusinessInvariantException

ORDER_NUMBER_REGEX = re.compile(r"^ORD-\d{8}-\d{4}$")


def validate_order_number(order_number: str) -> None:
    """Validate order number follows DEC-03: ORD-YYYYMMDD-XXXX."""
    if not ORDER_NUMBER_REGEX.match(order_number):
        raise BusinessInvariantException(
            f"Nomor pesanan '{order_number}' tidak sesuai format resmi: ORD-YYYYMMDD-XXXX."
        )


def validate_completion_time(estimated_completion_at: datetime) -> None:
    now = datetime.now(UTC)
    # Ensure timezone aware
    if estimated_completion_at.tzinfo is None:
        estimated_completion_at = estimated_completion_at.replace(tzinfo=UTC)
    if estimated_completion_at <= now:
        raise BusinessInvariantException(
            "Estimasi waktu selesai (estimated_completion_at) harus berada di masa depan."
        )
