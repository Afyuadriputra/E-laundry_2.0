import React, { useState } from 'react';
import { AlertTriangle, X } from 'lucide-react';
import { paymentsApi } from '../../services/payments';
import type { Payment } from '../../types/payments';

interface PaymentVoidModalProps {
  payment: Payment;
  onSuccess: (updatedPayment: Payment) => void;
  onClose: () => void;
}

export const PaymentVoidModal: React.FC<PaymentVoidModalProps> = ({
  payment,
  onSuccess,
  onClose,
}) => {
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reason.trim()) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const result = await paymentsApi.voidPayment(payment.id, { reason: reason.trim() });
      onSuccess(result);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal membatalkan pembayaran.';
      setErrorMessage(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-sm w-full p-6 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
          <div className="flex items-center gap-2 text-rose-700">
            <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
            <h3 className="text-base font-bold text-slate-900">Batalkan (Void) Pembayaran</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMessage && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700">
            {errorMessage}
          </div>
        )}

        <div className="mb-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-slate-500">Nominal:</span>
            <span className="font-bold text-slate-900">Rp {payment.amount.toLocaleString('id-ID')}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Metode:</span>
            <span className="font-medium text-slate-700">{payment.method}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Diverifikasi Oleh:</span>
            <span className="font-medium text-slate-700">{payment.verified_by_name || '-'}</span>
          </div>
        </div>

        <p className="text-xs text-slate-600 mb-3 leading-relaxed">
          Pembatalan tidak menghapus data historis, namun akan mengurangkan total terbayar dan mengembalikan status sisa piutang.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Alasan Pembatalan (Wajib)
            </label>
            <textarea
              rows={3}
              placeholder="Misal: Salah input nominal kasir / Transfer dibatalkan nasabah"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-rose-500/20 focus:border-rose-600"
            />
          </div>

          <div className="pt-2 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100 rounded-xl"
            >
              Kembali
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !reason.trim()}
              className="px-4 py-2 text-xs font-semibold text-white bg-rose-700 hover:bg-rose-800 disabled:opacity-50 rounded-xl shadow-sm"
            >
              {isSubmitting ? 'Memproses...' : 'Ya, Batalkan Pembayaran'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

