import React, { useEffect, useState } from 'react';
import type {
  OrderDetail,
  OperationalStatus,
  OrderTransitionInput,
} from '../../types/orders';
import { apiClient, type ApiResponse } from '../../lib/api-client';
import { useAuth } from '../../context/use-auth';
import { paymentsApi } from '../../services/payments';
import type { OrderPaymentSummary, Payment } from '../../types/payments';
import { PaymentModal } from '../payments/payment-modal';
import { PaymentVoidModal } from '../payments/payment-void-modal';
import { InvoiceModal } from '../invoices/invoice-modal';
import {
  ArrowLeft,
  Calendar,
  CheckCircle2,
  Clock,
  FileText,
  Flame,
  Loader2,
  MapPin,
  Phone,
  RefreshCw,
  ShoppingBag,
  Truck,
  User,
  X,
  XCircle,
  CreditCard,
  Ban,
  Share2,
} from 'lucide-react';

interface OrderDetailPageProps {
  orderId: string;
  onBack: () => void;
}

export const OrderDetailPage: React.FC<OrderDetailPageProps> = ({ orderId, onBack }) => {
  const { user } = useAuth();
  const isOwner = user?.role === 'OWNER';
  const isOwnerOrCashier = user?.role === 'OWNER' || user?.role === 'CASHIER';

  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [paymentSummary, setPaymentSummary] = useState<OrderPaymentSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Transition / Action state
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  // Modals state
  const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
  const [cancelReason, setCancelReason] = useState('');
  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);
  const [isInvoiceModalOpen, setIsInvoiceModalOpen] = useState(false);
  const [voidingPayment, setVoidingPayment] = useState<Payment | null>(null);

  const fetchOrderDetail = async () => {
    try {
      const [orderRes, payRes] = await Promise.all([
        apiClient<ApiResponse<OrderDetail>>(`/orders/${orderId}`),
        paymentsApi.getOrderPaymentSummary(orderId).catch(() => null),
      ]);
      setOrder(orderRes.data);
      if (payRes) setPaymentSummary(payRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Gagal memuat detail pesanan');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const [orderRes, payRes] = await Promise.all([
          apiClient<ApiResponse<OrderDetail>>(`/orders/${orderId}`),
          paymentsApi.getOrderPaymentSummary(orderId).catch(() => null),
        ]);
        if (!ignore) {
          setOrder(orderRes.data);
          if (payRes) setPaymentSummary(payRes);
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : 'Gagal memuat detail pesanan');
        }
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

  const handleTransition = async (nextStatus: OperationalStatus, reason?: string) => {
    if (!order) return;
    setActionError(null);
    setIsTransitioning(true);

    try {
      const payload: OrderTransitionInput = {
        to_status: nextStatus,
        reason: reason || `Transisi status ke ${nextStatus}`,
        expected_version: order.version,
      };

      const res = await apiClient<ApiResponse<OrderDetail>>(`/orders/${orderId}/transition`, {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      setOrder(res.data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal mengubah status pengerjaan';
      setActionError(msg);
    } finally {
      setIsTransitioning(false);
    }
  };

  const handleCancelOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!order || !cancelReason.trim()) return;

    setActionError(null);
    setIsTransitioning(true);

    try {
      const res = await apiClient<ApiResponse<OrderDetail>>(`/orders/${orderId}/cancel`, {
        method: 'POST',
        body: JSON.stringify({ reason: cancelReason }),
      });
      setOrder(res.data);
      setIsCancelModalOpen(false);
      setCancelReason('');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal membatalkan pesanan';
      setActionError(msg);
    } finally {
      setIsTransitioning(false);
    }
  };

  const formatRupiah = (val: number) => `Rp ${val.toLocaleString('id-ID')}`;

  const getStatusBadge = (status: OperationalStatus) => {
    switch (status) {
      case 'RECEIVED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-800">Diterima Kasir</span>;
      case 'QUEUED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800">Dalam Antrean</span>;
      case 'WASHING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-100 text-cyan-800">Sedang Dicuci</span>;
      case 'DRYING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Pengeringan</span>;
      case 'IRONING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-orange-100 text-orange-800">Penyetrikaan</span>;
      case 'QC_PACKING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-800">QC & Packing</span>;
      case 'READY':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">Siap Ambil/Antar</span>;
      case 'COMPLETED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-green-100 text-green-800">Selesai (Diserahkan)</span>;
      case 'CANCELLED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800">Dibatalkan</span>;
      default:
        return null;
    }
  };

  const getPaymentBadge = (status?: string) => {
    switch (status) {
      case 'PAID':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">LUNAS</span>;
      case 'PARTIALLY_PAID':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">DP / SEBAGIAN</span>;
      case 'UNPAID':
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800">BELUM LUNAS</span>;
    }
  };

  if (isLoading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin text-teal-700 mb-2" />
        <p className="text-sm font-semibold">Memuat rincian pesanan...</p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="p-8 text-center bg-white rounded-2xl border border-slate-200">
        <XCircle className="w-10 h-10 text-rose-500 mx-auto mb-2" />
        <h3 className="text-base font-bold text-slate-900">Pesanan Tidak Ditemukan</h3>
        <p className="text-xs text-slate-500 mt-1">{error || 'Data pesanan tidak dapat diakses.'}</p>
        <button
          onClick={onBack}
          className="mt-4 px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-700"
        >
          Kembali ke Daftar Pesanan
        </button>
      </div>
    );
  }

  const anyRequiresIroning = order.items.some((i) => i.requires_ironing_snapshot);

  return (
    <div className="space-y-6">
      {/* Top Navigation & Order Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 min-h-[44px] min-w-[44px] flex items-center justify-center transition-colors"
            title="Kembali"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-xl font-black text-slate-900 tracking-tight font-mono">
                {order.order_number}
              </h2>
              {getStatusBadge(order.operational_status)}
              <span className="text-[11px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">
                v{order.version}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1 flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>Dibuat: {new Date(order.created_at).toLocaleString('id-ID')}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setIsInvoiceModalOpen(true)}
            className="px-3.5 py-2.5 rounded-xl border border-teal-200 bg-teal-50 text-teal-800 hover:bg-teal-100 text-xs font-semibold min-h-[44px] flex items-center gap-1.5 shadow-xs transition-colors"
          >
            <Share2 className="w-4 h-4 text-teal-700" />
            <span>Nota & WhatsApp</span>
          </button>

          <button
            onClick={fetchOrderDetail}
            className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 min-h-[44px] min-w-[44px] flex items-center justify-center"
            title="Muat ulang"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          {isOwnerOrCashier && order.operational_status !== 'COMPLETED' && order.operational_status !== 'CANCELLED' && (
            <button
              onClick={() => setIsCancelModalOpen(true)}
              className="px-3.5 py-2.5 rounded-xl border border-rose-200 text-rose-700 hover:bg-rose-50 text-xs font-semibold min-h-[44px]"
            >
              Batalkan Pesanan
            </button>
          )}
        </div>
      </div>

      {actionError && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center gap-2">
          <XCircle className="w-5 h-5 shrink-0" />
          <span>{actionError}</span>
        </div>
      )}

      {/* Operational Workflow Progress Card */}
      {order.operational_status !== 'CANCELLED' && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center justify-between">
            <span>Alur Operasional Pengerjaan</span>
            {isTransitioning && <Loader2 className="w-4 h-4 animate-spin text-teal-700" />}
          </h3>

          <div className="flex flex-wrap gap-2">
            {order.operational_status === 'RECEIVED' && (
              <button
                onClick={() => handleTransition('QUEUED', 'Antrean cuci dimulai')}
                disabled={isTransitioning}
                className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
              >
                1. Masukkan ke Antrean (QUEUED)
              </button>
            )}

            {order.operational_status === 'QUEUED' && (
              <button
                onClick={() => handleTransition('WASHING', 'Mulai dicuci dalam mesin')}
                disabled={isTransitioning}
                className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
              >
                2. Mulai Cuci (WASHING)
              </button>
            )}

            {order.operational_status === 'WASHING' && (
              <button
                onClick={() => handleTransition('DRYING', 'Pindah ke mesin pengering')}
                disabled={isTransitioning}
                className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
              >
                3. Masukkan Pengering (DRYING)
              </button>
            )}

            {order.operational_status === 'DRYING' && (
              <>
                {anyRequiresIroning ? (
                  <button
                    onClick={() => handleTransition('IRONING', 'Pindah ke meja setrika')}
                    disabled={isTransitioning}
                    className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
                  >
                    4. Mulai Setrika (IRONING)
                  </button>
                ) : (
                  <button
                    onClick={() => handleTransition('QC_PACKING', 'Lewati setrika langsung QC')}
                    disabled={isTransitioning}
                    className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
                  >
                    4. QC & Packing (Tanpa Setrika)
                  </button>
                )}
              </>
            )}

            {order.operational_status === 'IRONING' && (
              <button
                onClick={() => handleTransition('QC_PACKING', 'Selesai setrika, QC & packing')}
                disabled={isTransitioning}
                className="px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[44px]"
              >
                5. Selesai Setrika & Packing (QC_PACKING)
              </button>
            )}

            {order.operational_status === 'QC_PACKING' && (
              <button
                onClick={() => handleTransition('READY', 'Pakaian siap diambil / diantar')}
                disabled={isTransitioning}
                className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs min-h-[44px]"
              >
                6. Tandai Siap Serah Terima (READY)
              </button>
            )}

            {order.operational_status === 'READY' && (
              <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium w-full flex items-center justify-between">
                <span>
                  ✓ Cucian telah selesai dan siap di rak pengambilan kasir / diantar kurir.
                  Penyelesaian status <strong>COMPLETED</strong> memerlukan pencatatan pelunasan nota dan konfirmasi serah terima fisik.
                </span>
              </div>
            )}

            {order.operational_status === 'COMPLETED' && (
              <div className="p-3 rounded-xl bg-slate-50 text-slate-600 text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Pesanan telah diserahkan kepada pelanggan dan berstatus selesai.</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Grid: Customer & Items */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Customer & Delivery details */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
              <User className="w-4 h-4 text-teal-700" />
              <span>Pelanggan</span>
            </h3>
            <div className="space-y-2 text-xs">
              <div className="font-bold text-slate-900 text-sm">{order.customer.full_name}</div>
              <div className="flex items-center gap-2 text-slate-600 font-mono">
                <Phone className="w-3.5 h-3.5 text-teal-700 shrink-0" />
                <span>{order.customer.phone_e164}</span>
              </div>
              {order.customer.address && (
                <div className="flex items-start gap-2 text-slate-600">
                  <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                  <span>{order.customer.address}</span>
                </div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
              <Truck className="w-4 h-4 text-teal-700" />
              <span>Metode Layanan</span>
            </h3>
            <div className="space-y-2 text-xs text-slate-600">
              <div className="flex justify-between">
                <span>Penerimaan:</span>
                <span className="font-semibold text-slate-800">
                  {order.intake_method === 'DROP_OFF' ? 'Antar Sendiri (Drop-off)' : 'Dijemput Kurir'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Pengambilan:</span>
                <span className="font-semibold text-slate-800">
                  {order.return_method === 'SELF_PICKUP' ? 'Ambil di Kasir' : 'Diantar ke Rumah'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Estimasi Selesai:</span>
                <span className="font-semibold text-slate-800">
                  {new Date(order.estimated_completion_at).toLocaleString('id-ID')}
                </span>
              </div>
            </div>
          </div>

          {order.customer_notes && (
            <div className="bg-amber-50/50 rounded-2xl border border-amber-200/60 p-4 text-xs text-amber-900 space-y-1">
              <div className="font-bold flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-amber-700" />
                <span>Catatan Pelanggan:</span>
              </div>
              <p className="italic">{order.customer_notes}</p>
            </div>
          )}
        </div>

        {/* Right Column (2 cols): Items, Payment Ledger & History */}
        <div className="md:col-span-2 space-y-6">
          {/* Services Items Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
              <ShoppingBag className="w-4 h-4 text-teal-700" />
              <span>Rincian Layanan ({order.items.length} Item)</span>
            </h3>

            <div className="divide-y divide-slate-100">
              {order.items.map((item) => (
                <div key={item.id} className="py-3 flex items-center justify-between gap-4">
                  <div>
                    <div className="font-bold text-slate-900 text-sm flex items-center gap-2">
                      <span>{item.service_name_snapshot}</span>
                      {item.requires_ironing_snapshot && (
                        <span title="Termasuk Setrika">
                          <Flame className="w-3.5 h-3.5 text-amber-600" />
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-slate-500 font-mono mt-0.5">
                      {item.quantity} {item.unit_snapshot} × {formatRupiah(item.unit_price_snapshot)}
                    </div>
                  </div>
                  <div className="font-bold text-slate-900 text-sm font-mono">
                    {formatRupiah(item.line_total_amount)}
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-slate-200 space-y-2 text-xs">
              <div className="flex justify-between text-slate-500">
                <span>Subtotal Layanan:</span>
                <span className="font-mono">{formatRupiah(order.subtotal_amount)}</span>
              </div>
              {order.extra_charge_amount > 0 && (
                <div className="flex justify-between text-slate-500">
                  <span>Biaya Tambahan / Express:</span>
                  <span className="font-mono">{formatRupiah(order.extra_charge_amount)}</span>
                </div>
              )}
              {order.delivery_fee_amount > 0 && (
                <div className="flex justify-between text-slate-500">
                  <span>Ongkir / Biaya Antar:</span>
                  <span className="font-mono">{formatRupiah(order.delivery_fee_amount)}</span>
                </div>
              )}
              <div className="flex justify-between text-base font-black text-slate-900 pt-2 border-t border-slate-100">
                <span>Total Tagihan:</span>
                <span className="font-mono text-teal-800">{formatRupiah(order.total_amount)}</span>
              </div>
            </div>
          </div>

          {/* Payment & Invoicing Card (M3) */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <CreditCard className="w-4 h-4 text-teal-700" />
                <h3 className="text-sm font-bold text-slate-900">Pembayaran & Status Tagihan</h3>
                {getPaymentBadge(paymentSummary?.payment_status)}
              </div>

              {isOwnerOrCashier &&
                order.operational_status !== 'CANCELLED' &&
                (paymentSummary?.remaining_amount ?? 1) > 0 && (
                  <button
                    type="button"
                    onClick={() => setIsPaymentModalOpen(true)}
                    className="px-3.5 py-2 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs min-h-[40px] flex items-center gap-1.5 shadow-sm transition-colors self-start sm:self-auto"
                  >
                    <CreditCard className="w-3.5 h-3.5" />
                    <span>Catat Pembayaran</span>
                  </button>
                )}
            </div>

            {/* Financial Ledger Highlights */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/60">
                <span className="text-[11px] font-semibold text-slate-500 uppercase">Total Tagihan</span>
                <div className="text-sm font-bold text-slate-900 font-mono mt-0.5">
                  {formatRupiah(order.total_amount)}
                </div>
              </div>
              <div className="p-3.5 rounded-xl bg-emerald-50/60 border border-emerald-100">
                <span className="text-[11px] font-semibold text-emerald-700 uppercase">Total Terbayar</span>
                <div className="text-sm font-bold text-emerald-800 font-mono mt-0.5">
                  {formatRupiah(paymentSummary?.total_paid || 0)}
                </div>
              </div>
              <div className="p-3.5 rounded-xl bg-rose-50/60 border border-rose-100">
                <span className="text-[11px] font-semibold text-rose-700 uppercase">Sisa Tagihan</span>
                <div className="text-sm font-bold text-rose-800 font-mono mt-0.5">
                  {formatRupiah(paymentSummary?.remaining_amount ?? order.total_amount)}
                </div>
              </div>
            </div>

            {/* Payment Transactions Table */}
            <div>
              <h4 className="text-xs font-bold text-slate-700 mb-2">Riwayat Transaksi Masuk</h4>
              {!paymentSummary?.payments || paymentSummary.payments.length === 0 ? (
                <div className="p-4 text-center rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-500">
                  Belum ada pembayaran yang dicatat untuk pesanan ini.
                </div>
              ) : (
                <div className="border border-slate-200 rounded-xl overflow-hidden">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-200">
                      <tr>
                        <th className="p-2.5">Waktu</th>
                        <th className="p-2.5">Metode</th>
                        <th className="p-2.5">Nominal</th>
                        <th className="p-2.5">Diverifikasi</th>
                        <th className="p-2.5">Status</th>
                        {isOwner && <th className="p-2.5 text-center">Aksi</th>}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {paymentSummary.payments.map((p) => (
                        <tr key={p.id} className={p.is_voided ? 'bg-slate-50 opacity-60' : ''}>
                          <td className="p-2.5 text-slate-700 whitespace-nowrap">
                            {new Date(p.payment_time).toLocaleString('id-ID')}
                          </td>
                          <td className="p-2.5 font-medium text-slate-800">{p.method}</td>
                          <td className="p-2.5 font-bold font-mono text-slate-900">
                            {formatRupiah(p.amount)}
                          </td>
                          <td className="p-2.5 text-slate-600">{p.verified_by_name || '-'}</td>
                          <td className="p-2.5">
                            {p.is_voided ? (
                              <span
                                className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800"
                                title={`Alasan: ${p.void_reason || '-'}`}
                              >
                                VOID (Batal)
                              </span>
                            ) : (
                              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                                Sah
                              </span>
                            )}
                          </td>
                          {isOwner && (
                            <td className="p-2.5 text-center">
                              {!p.is_voided && (
                                <button
                                  type="button"
                                  onClick={() => setVoidingPayment(p)}
                                  className="p-1 rounded-md text-rose-600 hover:bg-rose-50 hover:text-rose-800 transition-colors"
                                  title="Batalkan (Void) pembayaran ini"
                                >
                                  <Ban className="w-3.5 h-3.5" />
                                </button>
                              )}
                            </td>
                          )}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* Status History Timeline */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
              <Clock className="w-4 h-4 text-teal-700" />
              <span>Riwayat Transisi Status</span>
            </h3>

            <div className="space-y-4">
              {order.status_history.map((hist) => (
                <div key={hist.id} className="flex items-start gap-3 text-xs">
                  <div className="w-2 h-2 rounded-full bg-teal-600 mt-1.5 shrink-0" />
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-800">{hist.to_status}</span>
                      <span className="text-slate-400">
                        {new Date(hist.created_at).toLocaleTimeString('id-ID', {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </div>
                    {hist.reason && <p className="text-slate-500 mt-0.5">{hist.reason}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Payment Intake Modal */}
      {isPaymentModalOpen && paymentSummary && (
        <PaymentModal
          orderId={order.id}
          orderNumber={order.order_number}
          remainingAmount={paymentSummary.remaining_amount}
          onSuccess={() => {
            setIsPaymentModalOpen(false);
            fetchOrderDetail();
          }}
          onClose={() => setIsPaymentModalOpen(false)}
        />
      )}

      {/* Payment Void Modal */}
      {voidingPayment && (
        <PaymentVoidModal
          payment={voidingPayment}
          onSuccess={() => {
            setVoidingPayment(null);
            fetchOrderDetail();
          }}
          onClose={() => setVoidingPayment(null)}
        />
      )}

      {/* Digital Invoice Modal */}
      {isInvoiceModalOpen && (
        <InvoiceModal orderId={order.id} onClose={() => setIsInvoiceModalOpen(false)} />
      )}

      {/* Cancel Order Modal */}
      {isCancelModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">Batalkan Pesanan</h3>
              <button
                onClick={() => setIsCancelModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCancelOrder} className="space-y-4">
              <p className="text-xs text-slate-500 leading-relaxed">
                Pembatalan pesanan bersifat permanen dan akan dicatat ke dalam audit trail sistem.
              </p>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Alasan Pembatalan <span className="text-rose-500">*</span>
                </label>
                <textarea
                  required
                  rows={3}
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  placeholder="Contoh: Pelanggan meminta dibatalkan karena pakaian keliru dibawa..."
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500"
                />
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsCancelModalOpen(false)}
                  className="px-4 py-2.5 rounded-xl text-slate-600 hover:bg-slate-100 text-sm font-semibold min-h-[44px]"
                >
                  Kembali
                </button>
                <button
                  type="submit"
                  disabled={isTransitioning || !cancelReason.trim()}
                  className="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold min-h-[44px] flex items-center gap-2 disabled:opacity-50"
                >
                  {isTransitioning && <Loader2 className="w-4 h-4 animate-spin" />}
                  <span>Konfirmasi Batal</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
