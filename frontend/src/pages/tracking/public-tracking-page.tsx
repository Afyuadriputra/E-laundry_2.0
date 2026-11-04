import React, { useEffect, useState } from 'react';
import {
  Clock,
  MapPin,
  MessageCircle,
  PackageCheck,
  XCircle,
  CheckCircle2,
  Loader2,
  Store,
  CreditCard,
  UserCheck,
} from 'lucide-react';
import { trackingApi } from '../../services/tracking';
import type { PublicTrackingRead } from '../../types/tracking';

const STEPPER_STAGES = [
  { key: 'RECEIVED', label: 'Diterima' },
  { key: 'QUEUED', label: 'Antrean' },
  { key: 'WASHING', label: 'Cuci' },
  { key: 'DRYING', label: 'Kering' },
  { key: 'IRONING', label: 'Setrika' },
  { key: 'QC_PACKING', label: 'QC & Packing' },
  { key: 'READY', label: 'Siap Ambil' },
  { key: 'COMPLETED', label: 'Selesai' },
];

const STAGE_ORDER: Record<string, number> = {
  RECEIVED: 0,
  QUEUED: 1,
  WASHING: 2,
  DRYING: 3,
  IRONING: 4,
  QC_PACKING: 5,
  READY: 6,
  COMPLETED: 7,
};

interface PublicTrackingPageProps {
  token: string;
}

export const PublicTrackingPage: React.FC<PublicTrackingPageProps> = ({ token }) => {
  const [data, setData] = useState<PublicTrackingRead | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const res = await trackingApi.getTrackingData(token);
        if (!ignore) {
          setData(res);
          setIsLoading(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          const msg =
            err instanceof Error
              ? err.message
              : 'Tautan tracking tidak valid, telah kedaluwarsa, atau telah dinonaktifkan.';
          setErrorMessage(msg);
          setIsLoading(false);
        }
      }
    }
    load();
    return () => {
      ignore = true;
    };
  }, [token]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <Loader2 className="w-10 h-10 animate-spin text-teal-700 mb-3" />
        <p className="text-sm font-semibold text-slate-700">Memuat status pesanan...</p>
        <p className="text-xs text-slate-400 mt-1">Mengambil data terbaru dari sistem laundry</p>
      </div>
    );
  }

  if (errorMessage || !data) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl border border-slate-200 p-8 shadow-sm text-center">
          <div className="w-14 h-14 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto mb-4">
            <XCircle className="w-8 h-8" />
          </div>
          <h2 className="text-lg font-bold text-slate-900 mb-2">Tautan Tidak Ditemukan</h2>
          <p className="text-xs text-slate-600 leading-relaxed mb-6">
            {errorMessage || 'Tautan tracking ini salah, sudah kedaluwarsa, atau sudah dicabut.'}
          </p>
          <a
            href="/"
            className="inline-flex items-center justify-center px-5 py-2.5 text-xs font-semibold text-white bg-teal-700 hover:bg-teal-800 rounded-xl min-h-[44px]"
          >
            Kembali ke Beranda
          </a>
        </div>
      </div>
    );
  }

  const isCancelled = data.current_status === 'CANCELLED';
  const currentStageIndex = STAGE_ORDER[data.current_status] ?? -1;

  return (
    <div className="min-h-screen bg-slate-50 pb-16">
      {/* Top Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
        <div className="max-w-xl mx-auto px-4 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-teal-700 text-white flex items-center justify-center">
              <Store className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-900 leading-tight">
                {data.business_contact.name}
              </h1>
              <p className="text-[11px] text-slate-500">Pelacakan Pesanan Resmi</p>
            </div>
          </div>
          <a
            href={data.business_contact.whatsapp_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 px-3.5 py-2.5 text-xs font-semibold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 rounded-xl min-h-[44px] transition-colors"
          >
            <MessageCircle className="w-4 h-4 text-emerald-600" />
            <span>Tanya Kasir</span>
          </a>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-xl mx-auto px-4 pt-4 space-y-4">
        {/* Order Status Hero Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <div>
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                Nomor Nota
              </span>
              <h2 className="text-lg font-mono font-black text-slate-900 tracking-tight">
                {data.order_number}
              </h2>
            </div>
            <span
              className={`px-3 py-1 rounded-full text-xs font-bold ${
                isCancelled
                  ? 'bg-rose-50 text-rose-700 border border-rose-200'
                  : data.current_status === 'COMPLETED'
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'bg-teal-50 text-teal-800 border border-teal-200'
              }`}
            >
              {data.status_label}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-3 border-t border-slate-100 text-xs">
            <div>
              <span className="text-slate-400 block mb-0.5">Waktu Masuk:</span>
              <span className="font-medium text-slate-800">
                {new Date(data.created_at).toLocaleDateString('id-ID', {
                  day: 'numeric',
                  month: 'short',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block mb-0.5">Estimasi Selesai:</span>
              <span className="font-medium text-slate-800 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-teal-600" />
                <span>
                  {data.estimated_completion_at
                    ? new Date(data.estimated_completion_at).toLocaleDateString('id-ID', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })
                    : 'Segera'}
                </span>
              </span>
            </div>
          </div>
        </div>

        {/* Progress Stepper / Timeline */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-1.5">
            <PackageCheck className="w-4 h-4 text-teal-700" />
            <span>Progres Pengerjaan</span>
          </h3>

          {isCancelled ? (
            <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-center">
              <XCircle className="w-8 h-8 text-rose-600 mx-auto mb-2" />
              <p className="text-sm font-bold text-rose-900">Pesanan Telah Dibatalkan</p>
              <p className="text-xs text-rose-700 mt-1">
                Pesanan ini tidak lagi diproses. Hubungi outlet jika terdapat pertanyaan.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {STEPPER_STAGES.map((stg, idx) => {
                const isPassed = currentStageIndex > idx;
                const isCurrent = currentStageIndex === idx;

                return (
                  <div key={stg.key} className="flex items-center gap-3">
                    <div
                      className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 transition-colors ${
                        isPassed
                          ? 'bg-emerald-600 text-white'
                          : isCurrent
                          ? 'bg-teal-700 text-white ring-4 ring-teal-700/20'
                          : 'bg-slate-100 text-slate-400'
                      }`}
                    >
                      {isPassed ? <CheckCircle2 className="w-4 h-4" /> : idx + 1}
                    </div>
                    <div className="flex-1 flex items-center justify-between">
                      <span
                        className={`text-xs ${
                          isCurrent
                            ? 'font-bold text-teal-900'
                            : isPassed
                            ? 'font-medium text-slate-700'
                            : 'text-slate-400'
                        }`}
                      >
                        {stg.label}
                      </span>
                      {isCurrent && (
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-teal-100 text-teal-800 animate-pulse">
                          Sedang Berjalan
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Customer & Privacy Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center gap-2 mb-3">
            <UserCheck className="w-4 h-4 text-teal-700" />
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Pelanggan & Privasi
            </h3>
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-slate-400 block mb-0.5">Nama:</span>
              <span className="font-semibold text-slate-800">{data.customer_name_masked}</span>
            </div>
            <div>
              <span className="text-slate-400 block mb-0.5">Telepon:</span>
              <span className="font-mono font-medium text-slate-800">
                {data.customer_phone_masked}
              </span>
            </div>
          </div>
        </div>

        {/* Items Summary Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
            Rincian Cucian
          </h3>
          <div className="divide-y divide-slate-100">
            {data.service_summary.map((item, i) => (
              <div key={i} className="py-2.5 flex items-center justify-between text-xs">
                <div>
                  <div className="font-semibold text-slate-800">{item.service_name}</div>
                  <div className="text-[11px] text-slate-400">
                    {item.quantity} {item.unit} × Rp {item.unit_price.toLocaleString('id-ID')}
                  </div>
                </div>
                <div className="font-bold text-slate-900">
                  Rp {item.line_total.toLocaleString('id-ID')}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Payment Summary Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <CreditCard className="w-4 h-4 text-teal-700" />
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                Status Pembayaran
              </h3>
            </div>
            <span
              className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                data.financial_summary.payment_status === 'PAID'
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'bg-amber-50 text-amber-700 border border-amber-200'
              }`}
            >
              {data.financial_summary.payment_status === 'PAID' ? 'LUNAS' : 'BELUM LUNAS'}
            </span>
          </div>

          <div className="space-y-1.5 text-xs">
            <div className="flex items-center justify-between text-slate-600">
              <span>Total Tagihan:</span>
              <span className="font-semibold text-slate-900">
                Rp {data.financial_summary.total_amount.toLocaleString('id-ID')}
              </span>
            </div>
            <div className="flex items-center justify-between text-slate-600">
              <span>Sudah Dibayar:</span>
              <span className="font-semibold text-emerald-700">
                Rp {data.financial_summary.paid_amount.toLocaleString('id-ID')}
              </span>
            </div>
            <div className="flex items-center justify-between pt-2 border-t border-slate-100">
              <span className="font-bold text-slate-900">Sisa Tagihan:</span>
              <span className="text-base font-black text-rose-700 font-mono">
                Rp {data.financial_summary.remaining_amount.toLocaleString('id-ID')}
              </span>
            </div>
          </div>
        </div>

        {/* Outlet Contact Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs text-xs space-y-2">
          <h3 className="font-bold text-slate-900 uppercase tracking-wider mb-2">Informasi Outlet</h3>
          <div className="flex items-start gap-2 text-slate-600">
            <MapPin className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
            <span>{data.business_contact.address}</span>
          </div>
        </div>

        {/* Contact Cashier for Cancellation or Changes (PRD §5.7 #9: Read-Only Tracking) */}
        {!isCancelled && data.current_status !== 'COMPLETED' && (
          <div className="pt-2">
            <a
              href={`${data.business_contact.whatsapp_url}&text=${encodeURIComponent(
                `Halo ${data.business_contact.name}, saya ingin mengajukan konfirmasi/perubahan untuk pesanan ${data.order_number}.`
              )}`}
              target="_blank"
              rel="noreferrer"
              className="w-full py-3 px-4 rounded-xl text-xs font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 min-h-[44px] transition-colors flex items-center justify-center gap-2 shadow-xs"
              data-testid="contact-cashier-btn"
            >
              <MessageCircle className="w-4 h-4 text-emerald-600" />
              <span>Hubungi Kasir untuk Perubahan / Pembatalan</span>
            </a>
            <p className="text-[11px] text-slate-400 text-center mt-1.5">
              Halaman pelacakan publik bersifat baca-saja. Perubahan atau pembatalan dilayani oleh petugas kasir.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};
