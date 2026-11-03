from app.modules.invoices.schemas import InvoiceRead


def render_thermal_receipt(invoice: InvoiceRead, width_chars: int = 32) -> str:
    """Renders plain text formatted for standard 58mm POS thermal printers (32 columns)."""
    sep = "=" * width_chars
    thin_sep = "-" * width_chars

    lines = [
        invoice.business_name.center(width_chars),
        invoice.business_address[:width_chars].center(width_chars),
        f"Telp: {invoice.business_phone}".center(width_chars),
        sep,
        f"Nota : {invoice.order_number}",
        f"Tgl  : {invoice.created_at.strftime('%d/%m/%Y %H:%M')}",
        f"Cust : {invoice.customer_name[:20]}",
        f"Telp : {invoice.customer_phone}",
        thin_sep,
    ]

    for it in invoice.items:
        lines.append(f"{it.service_name[:width_chars]}")
        qty_str = f"  {it.quantity} {it.unit} x {it.unit_price:,}"
        total_str = f"Rp {it.line_total:,}"
        space_len = max(1, width_chars - len(qty_str) - len(total_str))
        lines.append(f"{qty_str}{' ' * space_len}{total_str}")

    lines.append(thin_sep)

    def format_row(label: str, val: str) -> str:
        space = max(1, width_chars - len(label) - len(val))
        return f"{label}{' ' * space}{val}"

    lines.append(format_row("Subtotal", f"Rp {invoice.subtotal_amount:,}"))
    if invoice.extra_charge_amount > 0:
        lines.append(format_row("Biaya Tambahan", f"Rp {invoice.extra_charge_amount:,}"))
    if invoice.delivery_fee_amount > 0:
        lines.append(format_row("Ongkir", f"Rp {invoice.delivery_fee_amount:,}"))
    lines.append(sep)
    lines.append(format_row("TOTAL", f"Rp {invoice.total_amount:,}"))
    lines.append(format_row("DIBAYAR", f"Rp {invoice.total_paid:,}"))
    lines.append(format_row("SISA TAGIHAN", f"Rp {invoice.remaining_amount:,}"))
    lines.append(sep)
    lines.append(format_row("STATUS", invoice.payment_status))
    lines.append(thin_sep)
    lines.append("Est. Selesai:".center(width_chars))
    lines.append(invoice.estimated_completion_at.strftime('%d/%m/%Y %H:%M').center(width_chars))
    lines.append("")
    lines.append("Lacak Status Pesanan:".center(width_chars))
    lines.append(invoice.tracking_url.center(width_chars))
    lines.append("")
    lines.append("Terima kasih atas".center(width_chars))
    lines.append("kunjungan Anda!".center(width_chars))
    lines.append("\n\n")

    return "\n".join(lines)


def render_html_invoice(invoice: InvoiceRead) -> str:
    """Renders printable, clean HTML document suitable for web preview and PDF generation."""
    items_rows = "".join([
        f"""
        <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e2e8f0;">{it.service_name}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e2e8f0; text-align: center;">
                {it.quantity} {it.unit}
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">
                Rp {it.unit_price:,}
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 600;">
                Rp {it.line_total:,}
            </td>
        </tr>
        """
        for it in invoice.items
    ])

    badge_class = "badge-unpaid"
    if invoice.payment_status == "PAID":
        badge_class = "badge-paid"
    elif invoice.payment_status == "PARTIALLY_PAID":
        badge_class = "badge-partial"

    extra_row = ""
    if invoice.extra_charge_amount > 0:
        extra_row = (
            f'<tr><td style="text-align: right;">Biaya Tambahan:</td>'
            f'<td style="text-align: right;">Rp {invoice.extra_charge_amount:,}</td></tr>'
        )

    delivery_row = ""
    if invoice.delivery_fee_amount > 0:
        delivery_row = (
            f'<tr><td style="text-align: right;">Ongkir:</td>'
            f'<td style="text-align: right;">Rp {invoice.delivery_fee_amount:,}</td></tr>'
        )

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota {invoice.order_number}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 24px; color: #1e293b; background: #fff; }}
        .invoice-card {{ max-width: 600px; margin: 0 auto; border: 1px solid #cbd5e1; border-radius: 12px; padding: 28px; }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #0f766e; padding-bottom: 16px; margin-bottom: 20px; }}
        .biz-title {{ font-size: 20px; font-weight: bold; color: #0f766e; }}
        .biz-sub {{ font-size: 13px; color: #64748b; margin-top: 4px; }}
        .meta-table {{ width: 100%; margin-bottom: 20px; font-size: 14px; }}
        .meta-table td {{ padding: 4px 0; }}
        .items-table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 20px; }}
        .items-table th {{ background: #f8fafc; padding: 8px 12px; text-align: left; border-bottom: 2px solid #cbd5e1; color: #475569; }}
        .totals-table {{ width: 100%; font-size: 14px; }}
        .totals-table td {{ padding: 4px 8px; }}
        .grand-total {{ font-size: 16px; font-weight: bold; color: #0f766e; border-top: 2px solid #e2e8f0; padding-top: 8px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: bold; }}
        .badge-paid {{ background: #dcfce7; color: #166534; }}
        .badge-partial {{ background: #fef9c3; color: #854d0e; }}
        .badge-unpaid {{ background: #fee2e2; color: #991b1b; }}
        .footer {{ text-align: center; margin-top: 28px; font-size: 12px; color: #64748b; border-top: 1px dashed #cbd5e1; padding-top: 16px; }}
        @media print {{
            body {{ padding: 0; }}
            .invoice-card {{ border: none; padding: 0; max-width: 100%; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <div>
                <div class="biz-title">{invoice.business_name}</div>
                <div class="biz-sub">{invoice.business_address}</div>
                <div class="biz-sub">Telp: {invoice.business_phone}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 18px; font-weight: bold; color: #334155;">NOTA DIGITAL</div>
                <div style="font-size: 14px; font-weight: 600; color: #0f766e; margin-top: 4px;">{invoice.order_number}</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 2px;">{invoice.created_at.strftime('%d/%m/%Y %H:%M')}</div>
            </div>
        </div>

        <table class="meta-table">
            <tr>
                <td style="width: 50%;"><strong>Pelanggan:</strong> {invoice.customer_name} ({invoice.customer_phone})</td>
                <td style="width: 50%; text-align: right;"><strong>Estimasi Selesai:</strong> {invoice.estimated_completion_at.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
            <tr>
                <td><strong>Penerimaan:</strong> {invoice.intake_method} | <strong>Pengambilan:</strong> {invoice.return_method}</td>
                <td style="text-align: right;">
                    <strong>Status Bayar:</strong>
                    <span class="badge {badge_class}">
                        {invoice.payment_status}
                    </span>
                </td>
            </tr>
        </table>

        <table class="items-table">
            <thead>
                <tr>
                    <th>Layanan</th>
                    <th style="text-align: center;">Kuantitas</th>
                    <th style="text-align: right;">Tarif</th>
                    <th style="text-align: right;">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_rows}
            </tbody>
        </table>

        <table class="totals-table">
            <tr>
                <td style="text-align: right; width: 70%;">Subtotal:</td>
                <td style="text-align: right; font-weight: 500;">Rp {invoice.subtotal_amount:,}</td>
            </tr>
            {extra_row}
            {delivery_row}
            <tr>
                <td class="grand-total" style="text-align: right;">TOTAL TAGIHAN:</td>
                <td class="grand-total" style="text-align: right;">Rp {invoice.total_amount:,}</td>
            </tr>
            <tr>
                <td style="text-align: right; color: #166534; font-weight: 600;">Total Dibayar:</td>
                <td style="text-align: right; color: #166534; font-weight: 600;">Rp {invoice.total_paid:,}</td>
            </tr>
            <tr>
                <td style="text-align: right; color: #991b1b; font-weight: bold;">Sisa Tagihan:</td>
                <td style="text-align: right; color: #991b1b; font-weight: bold;">Rp {invoice.remaining_amount:,}</td>
            </tr>
        </table>

        <div class="footer">
            <p>Pantau status cucian Anda: <a href="{invoice.tracking_url}">{invoice.tracking_url}</a></p>
            <p>Terima kasih atas kepercayaan Anda kepada {invoice.business_name}!</p>
        </div>
    </div>
</body>
</html>
"""
