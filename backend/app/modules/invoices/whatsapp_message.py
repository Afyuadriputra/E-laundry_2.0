import urllib.parse
from datetime import datetime


def generate_whatsapp_message(
    business_name: str,
    order_number: str,
    customer_name: str,
    created_at: datetime,
    estimated_completion_at: datetime,
    items: list[dict],
    total_amount: int,
    total_paid: int,
    remaining_amount: int,
    payment_status: str,
    tracking_url: str,
) -> str:
    """Formats human-readable WhatsApp nota text according to IPD Section 12.7."""
    date_in = created_at.strftime("%d/%m/%Y %H:%M")
    date_est = estimated_completion_at.strftime("%d/%m/%Y %H:%M")

    status_id_map = {
        "PAID": "LUNAS",
        "PARTIALLY_PAID": "DP / SEBAGIAN",
        "UNPAID": "BELUM LUNAS",
    }
    status_label = status_id_map.get(payment_status, payment_status)

    lines = [
        f"*{business_name} - NOTA TRANSAKSI*",
        "--------------------------------",
        f"No. Nota: *{order_number}*",
        f"Pelanggan: {customer_name}",
        f"Tgl Terima: {date_in}",
        f"Est. Selesai: {date_est}",
        "",
        "*Rincian Layanan:*",
    ]

    for it in items:
        lines.append(f"• {it['name']} ({it['quantity']} {it['unit']}) : Rp {it['line_total']:,}")

    lines.extend([
        "",
        "--------------------------------",
        f"Total Tagihan : Rp {total_amount:,}",
        f"Total Dibayar : Rp {total_paid:,}",
        f"Sisa Tagihan  : *Rp {remaining_amount:,}*",
        f"Status Bayar  : *{status_label}*",
        "--------------------------------",
        "",
        "Pantau progres cucian Anda secara online melalui link berikut:",
        tracking_url,
        "",
        f"Terima kasih atas kepercayaan Anda kepada {business_name}!",
    ])

    return "\n".join(lines)


def build_whatsapp_deeplink(phone_e164: str, message: str) -> str:
    """Builds deep link `https://wa.me/{phone_without_plus}?text={encoded_message}`."""
    clean_digits = "".join(filter(str.isdigit, phone_e164))
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{clean_digits}?text={encoded}"
