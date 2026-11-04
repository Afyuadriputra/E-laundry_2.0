import React, { useEffect, useState } from 'react';
import {
  Printer,
  Share2,
  Copy,
  Check,
  X,
  FileText,
  Loader2,
} from 'lucide-react';
import { invoicesApi } from '../../services/invoices';
import type { Invoice } from '../../types/invoices';

interface InvoiceModalProps {
  orderId: string;
  onClose: () => void;
}

export const InvoiceModal: React.FC<InvoiceModalProps> = ({ orderId, onClose }) => {
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeView, setActiveView] = useState<'STANDARD' | 'THERMAL'>('STANDARD');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const data = await invoicesApi.getInvoice(orderId);
        if (!ignore) {
          setInvoice(data);
        }
      } catch (err) {
        console.error('Failed to load invoice', err);
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }
    load();
    return () => {
      ignore = true;
    };
  }, [orderId]);

  const handleCopyText = async () => {
    if (!invoice) return;
    try {
      await navigator.clipboard.writeText(invoice.whatsapp_share_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy', err);
    }
  };

  const handlePrint = () => {
    window.open(invoicesApi.getHtmlUrl(orderId), '_blank');
  };

  const handleOpenWhatsApp = () => {
    if (!invoice) return;
    window.open(invoice.whatsapp_share_url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-xl w-full p-6 animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-700" />
            <div>
              <h3 className="text-base font-bold text-slate-900">Nota Digital & Cetak</h3>
              {invoice && <p className="text-xs text-slate-500 font-mono">{invoice.order_number}</p>}
            </div>
          </div>
          <button
            onClick={onClose}
            className="min-h-[44px] min-w-[44px] flex items-center justify-center p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            title="Tutup modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {isLoading ? (
          <div className="py-16 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="w-8 h-8 animate-spin text-teal-700 mb-2" />
            <p className="text-xs">Memuat data nota...</p>
          </div>
        ) : !invoice ? (
          <div className="py-8 text-center text-rose-600 text-xs">Gagal memuat rincian nota.</div>
        ) : (
          <div className="space-y-4">
            {/* View Switcher Tabs */}
            <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
              <button
                type="button"
                onClick={() => setActiveView('STANDARD')}
                className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                  activeView === 'STANDARD'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Tampilan Nota Standar
              </button>
              <button
                type="button"
                onClick={() => setActiveView('THERMAL')}
                className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                  activeView === 'THERMAL'
                    ? 'bg-white text-slate-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Pratinjau POS Thermal (58mm)
              </button>
            </div>

            {/* Standard View */}
            {activeView === 'STANDARD' && (
              <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 space-y-3 text-xs">
                {/* Biz & Customer */}
                <div className="flex justify-between items-start pb-2 border-b border-slate-200">
                  <div>
                    <div className="font-bold text-sm text-teal-900">{invoice.business_name}</div>
                    <div className="text-slate-500">{invoice.business_address}</div>
                    <div className="text-slate-500">Telp: {invoice.business_phone}</div>
                  </div>
                  <div className="text-right">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                        invoice.payment_status === 'PAID'
                          ? 'bg-emerald-100 text-emerald-800'
                          : invoice.payment_status === 'PARTIALLY_PAID'
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-rose-100 text-rose-800'
                      }`}
                    >
                      {invoice.payment_status === 'PAID'
                        ? 'LUNAS'
                        : invoice.payment_status === 'PARTIALLY_PAID'
                        ? 'DP / SEBAGIAN'
                        : 'BELUM LUNAS'}
                    </span>
                    <div className="text-slate-500 mt-1 font-mono">{invoice.order_number}</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-slate-700">
                  <div>
                    <span className="text-slate-400">Pelanggan:</span>{' '}
                    <strong>{invoice.customer_name}</strong> ({invoice.customer_phone})
                  </div>
                  <div className="text-right">
                    <span className="text-slate-400">Est. Selesai:</span>{' '}
                    <strong>{new Date(invoice.estimated_completion_at).toLocaleString('id-ID')}</strong>
                  </div>
                </div>

                {/* Items Table */}
                <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-200">
                      <tr>
                        <th className="p-2">Layanan</th>
                        <th className="p-2 text-center">Qty</th>
                        <th className="p-2 text-right">Tarif</th>
                        <th className="p-2 text-right">Total</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {invoice.items.map((it, idx) => (
                        <tr key={idx}>
                          <td className="p-2 font-medium text-slate-900">{it.service_name}</td>
                          <td className="p-2 text-center">
                            {it.quantity} {it.unit}
                          </td>
                          <td className="p-2 text-right">Rp {it.unit_price.toLocaleString('id-ID')}</td>
                          <td className="p-2 text-right font-semibold">Rp {it.line_total.toLocaleString('id-ID')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Totals Breakdown */}
                <div className="space-y-1 pt-1 border-t border-slate-200">
                  <div className="flex justify-between text-slate-600">
                    <span>Subtotal:</span>
                    <span>Rp {invoice.subtotal_amount.toLocaleString('id-ID')}</span>
                  </div>
                  {invoice.extra_charge_amount > 0 && (
                    <div className="flex justify-between text-slate-600">
                      <span>Biaya Tambahan:</span>
                      <span>Rp {invoice.extra_charge_amount.toLocaleString('id-ID')}</span>
                    </div>
                  )}
                  {invoice.delivery_fee_amount > 0 && (
                    <div className="flex justify-between text-slate-600">
                      <span>Ongkir:</span>
                      <span>Rp {invoice.delivery_fee_amount.toLocaleString('id-ID')}</span>
                    </div>
                  )}
                  <div className="flex justify-between font-bold text-sm text-slate-900 pt-1 border-t border-slate-200">
                    <span>Total Tagihan:</span>
                    <span>Rp {invoice.total_amount.toLocaleString('id-ID')}</span>
                  </div>
                  <div className="flex justify-between text-emerald-700 font-semibold">
                    <span>Total Terbayar:</span>
                    <span>Rp {invoice.total_paid.toLocaleString('id-ID')}</span>
                  </div>
                  <div className="flex justify-between text-rose-700 font-bold">
                    <span>Sisa Tagihan:</span>
                    <span>Rp {invoice.remaining_amount.toLocaleString('id-ID')}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Thermal POS View */}
            {activeView === 'THERMAL' && (
              <div className="border border-slate-200 rounded-xl p-4 bg-slate-900 text-slate-100 font-mono text-xs whitespace-pre-wrap max-h-72 overflow-y-auto">
                {`================================
${invoice.business_name.toUpperCase().padStart(26)}
${invoice.business_phone.padStart(24)}
================================
No. Nota : ${invoice.order_number}
Tgl      : ${new Date(invoice.created_at).toLocaleDateString('id-ID')}
Pelanggan: ${invoice.customer_name}
Telp     : ${invoice.customer_phone}
--------------------------------
${invoice.items
  .map(
    (it) =>
      `${it.service_name}\n  ${it.quantity} ${it.unit} x ${it.unit_price} = Rp ${it.line_total.toLocaleString('id-ID')}`
  )
  .join('\n')}
--------------------------------
TOTAL    : Rp ${invoice.total_amount.toLocaleString('id-ID')}
DIBAYAR  : Rp ${invoice.total_paid.toLocaleString('id-ID')}
SISA     : Rp ${invoice.remaining_amount.toLocaleString('id-ID')}
STATUS   : ${invoice.payment_status}
================================
Lacak Pesanan:
${invoice.tracking_url}
Terima kasih!
`}
              </div>
            )}

            {/* Actions Toolbar */}
            <div className="pt-2 flex flex-wrap items-center justify-between gap-2 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handlePrint}
                  className="min-h-[44px] px-3.5 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl flex items-center gap-1.5 transition-colors"
                >
                  <Printer className="w-4 h-4 text-slate-500" />
                  <span>Cetak Nota</span>
                </button>

                <button
                  type="button"
                  onClick={handleCopyText}
                  className="min-h-[44px] px-3.5 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl flex items-center gap-1.5 transition-colors"
                >
                  {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4 text-slate-500" />}
                  <span>{copied ? 'Tersalin!' : 'Salin Pesan'}</span>
                </button>
              </div>

              <button
                type="button"
                onClick={handleOpenWhatsApp}
                className="min-h-[44px] px-4 py-2.5 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl flex items-center gap-1.5 shadow-sm transition-colors"
              >
                <Share2 className="w-4 h-4" />
                <span>Kirim via WhatsApp</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
