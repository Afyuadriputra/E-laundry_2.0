import csv
import io
from typing import Any


def sanitize_csv_cell(value: Any) -> str:
    """
    Sanitize text to prevent CSV Formula Injection (CWE-1236).
    If a string cell starts with '=', '+', '-', '@', '\t', or '\r',
    prepend with a single quote (') to force literal interpretation.
    """
    if value is None:
        return ""
    val_str = str(value)
    if val_str and val_str[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{val_str}"
    return val_str


def generate_orders_csv(orders: list[dict[str, Any]]) -> str:
    """
    Generate sanitized RFC 4180 CSV for orders report.
    """
    output = io.StringIO()
    writer = csv.writer(output, dialect="excel")

    # Header
    writer.writerow([
        "No. Pesanan",
        "Tanggal Dibuat",
        "Nama Pelanggan",
        "No. Telepon",
        "Status Operasional",
        "Status Pembayaran",
        "Total Tagihan (Rp)",
        "Sudah Dibayar (Rp)",
        "Sisa Tagihan (Rp)",
        "Rincian Layanan",
    ])

    for ord in orders:
        writer.writerow([
            sanitize_csv_cell(ord.get("order_number")),
            sanitize_csv_cell(ord.get("created_at")),
            sanitize_csv_cell(ord.get("customer_name")),
            sanitize_csv_cell(ord.get("customer_phone")),
            sanitize_csv_cell(ord.get("operational_status")),
            sanitize_csv_cell(ord.get("payment_status")),
            ord.get("total_amount", 0),
            ord.get("paid_amount", 0),
            ord.get("remaining_amount", 0),
            sanitize_csv_cell(ord.get("items_summary")),
        ])

    return output.getvalue()


def generate_payments_csv(payments: list[dict[str, Any]]) -> str:
    """
    Generate sanitized RFC 4180 CSV for payments report.
    """
    output = io.StringIO()
    writer = csv.writer(output, dialect="excel")

    # Header
    writer.writerow([
        "ID Pembayaran",
        "Waktu Pembayaran",
        "No. Pesanan",
        "Metode Pembayaran",
        "Jumlah (Rp)",
        "Status Validitas",
        "Referensi / Catatan",
    ])

    for p in payments:
        writer.writerow([
            sanitize_csv_cell(p.get("id")),
            sanitize_csv_cell(p.get("created_at")),
            sanitize_csv_cell(p.get("order_number")),
            sanitize_csv_cell(p.get("payment_method")),
            p.get("amount", 0),
            "BATAL / VOID" if p.get("is_voided") else "SAH",
            sanitize_csv_cell(p.get("notes")),
        ])

    return output.getvalue()


def generate_expenses_csv(expenses: list[dict[str, Any]]) -> str:
    """
    Generate sanitized RFC 4180 CSV for expenses report.
    """
    output = io.StringIO()
    writer = csv.writer(output, dialect="excel")

    # Header
    writer.writerow([
        "ID Pengeluaran",
        "Tanggal",
        "Kategori",
        "Keterangan",
        "Jumlah (Rp)",
        "Dicatat Oleh",
    ])

    for exp in expenses:
        writer.writerow([
            sanitize_csv_cell(exp.get("id")),
            sanitize_csv_cell(exp.get("expense_date")),
            sanitize_csv_cell(exp.get("category")),
            sanitize_csv_cell(exp.get("description")),
            exp.get("amount", 0),
            sanitize_csv_cell(exp.get("created_by_name")),
        ])

    return output.getvalue()

