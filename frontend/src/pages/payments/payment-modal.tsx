import React, { useState } from 'react';
import { CreditCard, Banknote, QrCode, AlertCircle, CheckCircle2, X } from 'lucide-react';
import { paymentsApi } from '../../services/payments';
import type { PaymentMethod, Payment } from '../../types/payments';

interface PaymentModalProps {
  orderId: string;
  orderNumber: string;
  remainingAmount: number;
  onSuccess: (payment: Payment) => void;
  onClose: () => void;
}

export const PaymentModal: React.FC<PaymentModalProps> = ({
  orderId,
  orderNumber,
  remainingAmount,
  onSuccess,
  onClose,
}) => {
  const [method, setMethod] = useState<PaymentMethod>('CASH');
  const [amount, setAmount] = useState<number>(remainingAmount);
  const [cashTendered, setCashTendered] = useState<number>(remainingAmount);
  const [referenceNote, setReferenceNote] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const cashChange = method === 'CASH' ? Math.max(0, (cashTendered || 0) - (amount || 0)) : 0;
  const isOverpaid = amount > remainingAmount;
  const isZero = amount <= 0;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isOverpaid || isZero) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const idempotencyKey = `pay-${orderId}-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;
      const result = await paymentsApi.recordPayment(
        orderId,
        {
          amount,
          method,
          reference_note: referenceNote || undefined,
        },
        idempotencyKey
      );
      onSuccess(result);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal mencatat pembayaran.';
      setErrorMessage(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-900">Catat Pembayaran</h3>
            <p className="text-xs text-slate-500 font-mono mt-0.5">{orderNumber}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMessage && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate className="space-y-4">
          {/* Sisa Tagihan Badge */}
          <div className="p-3 rounded-xl bg-teal-50 border border-teal-100 flex items-center justify-between">
            <span className="text-xs font-semibold text-teal-800">Sisa Tagihan:</span>
            <span className="text-base font-bold text-teal-900">Rp {remainingAmount.toLocaleString('id-ID')}</span>
          </div>

          {/* Payment Method Selector */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">Metode Pembayaran</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setMethod('CASH')}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition-all ${
                  method === 'CASH'
                    ? 'border-teal-600 bg-teal-50/50 text-teal-800 ring-2 ring-teal-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Banknote className="w-5 h-5 mb-1" />
                <span>Tunai</span>
              </button>

              <button
                type="button"
                onClick={() => setMethod('BANK_TRANSFER')}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition-all ${
                  method === 'BANK_TRANSFER'
                    ? 'border-teal-600 bg-teal-50/50 text-teal-800 ring-2 ring-teal-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <CreditCard className="w-5 h-5 mb-1" />
                <span>Transfer</span>
              </button>

              <button
                type="button"
                onClick={() => setMethod('QRIS_MANUAL')}
                className={`flex flex-col items-center justify-center p-3 rounded-xl border text-xs font-semibold transition-all ${
                  method === 'QRIS_MANUAL'
                    ? 'border-teal-600 bg-teal-50/50 text-teal-800 ring-2 ring-teal-500/20'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <QrCode className="w-5 h-5 mb-1" />
                <span>QRIS Manual</span>
              </button>
            </div>
          </div>

          {/* Nominal Bayar */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-semibold text-slate-700">Nominal yang Dicatat (Rp)</label>
              <button
                type="button"
                onClick={() => {
                  setAmount(remainingAmount);
                  setCashTendered(remainingAmount);
                }}
                className="text-xs text-teal-700 font-semibold hover:underline"
              >
                Set Lunas Penuh
              </button>
            </div>
            <input
              type="number"
              min={1}
              max={remainingAmount}
              value={amount || ''}
              onChange={(e) => {
                const val = parseInt(e.target.value, 10) || 0;
                setAmount(val);
                if (method === 'CASH' && cashTendered < val) {
                  setCashTendered(val);
                }
              }}
              required
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
            />
            {isOverpaid && (
              <p className="text-xs text-rose-600 mt-1">
                Nominal tidak boleh melebihi sisa tagihan (Rp {remainingAmount.toLocaleString('id-ID')}).
              </p>
            )}
          </div>

          {/* Cash Change Calculator (only for Tunai) */}
          {method === 'CASH' && (
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/60 space-y-2">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Uang Diterima dari Pelanggan (Rp)</label>
                <input
                  type="number"
                  min={amount}
                  value={cashTendered || ''}
                  onChange={(e) => setCashTendered(parseInt(e.target.value, 10) || 0)}
                  className="w-full px-3 py-1.5 text-sm bg-white border border-slate-200 rounded-lg"
                />
              </div>

              <div className="flex items-center justify-between pt-1 border-t border-slate-200">
                <span className="text-xs font-semibold text-slate-700">Kembalian:</span>
                <span className="text-sm font-bold text-emerald-700">Rp {cashChange.toLocaleString('id-ID')}</span>
              </div>
            </div>
          )}

          {/* Reference Note */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Catatan / Bukti Ref (Opsional)</label>
            <input
              type="text"
              placeholder={method === 'CASH' ? 'Misal: Uang pas' : 'Misal: BCA an Andi / Ref QRIS 8921'}
              value={referenceNote}
              onChange={(e) => setReferenceNote(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl"
            />
          </div>

          {/* Submit Buttons */}
          <div className="pt-2 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100 rounded-xl"
            >
              Batal
            </button>
            <button
              type="submit"
              disabled={isSubmitting || isOverpaid || isZero}
              className="px-5 py-2 text-xs font-semibold text-white bg-teal-700 hover:bg-teal-800 disabled:opacity-50 rounded-xl flex items-center gap-1.5 shadow-sm"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>{isSubmitting ? 'Menyimpan...' : 'Konfirmasi Pembayaran'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
