import React, { useEffect, useState } from 'react';
import type { Customer } from '../../types/customers';
import type { LaundryService } from '../../types/services';
import type { IntakeMethod, OrderCreateInput, ReturnMethod } from '../../types/orders';
import { apiClient, type ApiResponse } from '../../lib/api-client';
import {
  ShoppingBag,
  User,
  Plus,
  Trash2,
  Truck,
  Check,
  AlertCircle,
  Loader2,
  Info,
  ArrowLeft,
} from 'lucide-react';

interface CreateOrderPageProps {
  onBack: () => void;
  onSuccess: (orderId: string) => void;
}

export const CreateOrderPage: React.FC<CreateOrderPageProps> = ({ onBack, onSuccess }) => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [services, setServices] = useState<LaundryService[]>([]);
  const [isLoadingMeta, setIsLoadingMeta] = useState(true);

  // Form State
  const [isNewCustomer, setIsNewCustomer] = useState(false);
  const [selectedCustomerId, setSelectedCustomerId] = useState('');
  const [newCustomerName, setNewCustomerName] = useState('');
  const [newCustomerPhone, setNewCustomerPhone] = useState('');
  const [newCustomerAddress, setNewCustomerAddress] = useState('');

  const [orderItems, setOrderItems] = useState<{ serviceId: string; quantity: string }[]>([
    { serviceId: '', quantity: '3.0' },
  ]);

  const [intakeMethod, setIntakeMethod] = useState<IntakeMethod>('DROP_OFF');
  const [returnMethod, setReturnMethod] = useState<ReturnMethod>('SELF_PICKUP');
  const [extraCharge, setExtraCharge] = useState(0);
  const [deliveryFee, setDeliveryFee] = useState(0);
  const [customerNotes, setCustomerNotes] = useState('');
  const [internalNotes, setInternalNotes] = useState('');

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const loadInitialData = async () => {
      setIsLoadingMeta(true);
      try {
        const [cRes, sRes] = await Promise.all([
          apiClient<ApiResponse<Customer[]>>('/customers?limit=100'),
          apiClient<ApiResponse<LaundryService[]>>('/services?is_active=true'),
        ]);
        setCustomers(cRes.data);
        setServices(sRes.data);
        if (sRes.data.length > 0) {
          setOrderItems([{ serviceId: sRes.data[0].id, quantity: '3.0' }]);
        }
      } catch (err) {
        setErrorMessage(err instanceof Error ? err.message : 'Gagal memuat data formulir');
      } finally {
        setIsLoadingMeta(false);
      }
    };
    loadInitialData();
  }, []);

  const handleAddItem = () => {
    if (services.length > 0) {
      setOrderItems([...orderItems, { serviceId: services[0].id, quantity: '1.0' }]);
    }
  };

  const handleRemoveItem = (index: number) => {
    if (orderItems.length > 1) {
      setOrderItems(orderItems.filter((_, i) => i !== index));
    }
  };

  const handleItemChange = (index: number, field: 'serviceId' | 'quantity', value: string) => {
    const updated = [...orderItems];
    updated[index][field] = value;
    setOrderItems(updated);
  };

  // Live Pricing Calculation Preview matching Python Decimal rules
  const calculateItemPreview = (serviceId: string, qtyStr: string) => {
    const service = services.find((s) => s.id === serviceId);
    if (!service) return { billableQty: 0, lineTotal: 0, note: '' };

    const parsedQty = parseFloat(qtyStr) || 0;
    if (parsedQty <= 0) return { billableQty: 0, lineTotal: 0, note: 'Kuantitas tidak valid' };

    if (service.pricing_type === 'PER_KG') {
      // Round to 0.1 kg (DEC-01)
      const rounded = Math.round(parsedQty * 10) / 10;
      // Enforce 3.0 kg floor (DEC-02)
      const billable = Math.max(rounded, 3.0);
      const total = Math.round(billable * service.unit_price);
      let note = '';
      if (rounded < 3.0) {
        note = 'Dikenakan minimum 3.0 kg per nota kiloan';
      } else if (rounded !== parsedQty) {
        note = `Dibulatkan ke ${rounded.toFixed(1)} kg`;
      }
      return { billableQty: billable, lineTotal: total, note };
    } else {
      const wholeQty = Math.floor(parsedQty);
      const total = wholeQty * service.unit_price;
      return { billableQty: wholeQty, lineTotal: total, note: `${wholeQty} Pcs` };
    }
  };

  const calculateSubtotal = () => {
    return orderItems.reduce((acc, item) => {
      const { lineTotal } = calculateItemPreview(item.serviceId, item.quantity);
      return acc + lineTotal;
    }, 0);
  };

  const subtotal = calculateSubtotal();
  const grandTotal = subtotal + (extraCharge || 0) + (deliveryFee || 0);

  const formatRupiah = (val: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(val);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      const payload: OrderCreateInput = {
        customer_id: isNewCustomer ? undefined : selectedCustomerId || undefined,
        new_customer_name: isNewCustomer ? newCustomerName.trim() : undefined,
        new_customer_phone: isNewCustomer ? newCustomerPhone.trim() : undefined,
        new_customer_address: isNewCustomer ? newCustomerAddress.trim() : undefined,
        items: orderItems.map((item) => ({
          service_id: item.serviceId,
          quantity: item.quantity,
        })),
        intake_method: intakeMethod,
        return_method: returnMethod,
        extra_charge_amount: extraCharge || 0,
        delivery_fee_amount: deliveryFee || 0,
        customer_notes: customerNotes.trim() || undefined,
        internal_notes: internalNotes.trim() || undefined,
      };

      const res = await apiClient<ApiResponse<{ id: string }>>('/orders', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      onSuccess(res.data.id);
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'Gagal membuat pesanan');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoadingMeta) {
    return (
      <div className="p-12 text-center">
        <Loader2 className="w-8 h-8 animate-spin text-teal-700 mx-auto mb-2" />
        <p className="text-sm text-slate-500">Memuat formulir kasir...</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button
          onClick={onBack}
          className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 min-h-[44px] min-w-[44px] flex items-center justify-center"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ShoppingBag className="w-6 h-6 text-teal-700" />
            <span>Penerimaan Pesanan Baru</span>
          </h2>
          <p className="text-xs text-slate-500">
            Kalkulasi otomatis bobot kiloan (0.1 kg HALF_UP) & batas minimal 3.0 kg.
          </p>
        </div>
      </div>

      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Section 1: Customer */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <User className="w-4 h-4 text-teal-700" />
              <span>Data Pelanggan</span>
            </h3>
            <button
              type="button"
              onClick={() => setIsNewCustomer(!isNewCustomer)}
              className="text-xs font-semibold text-teal-700 hover:text-teal-800"
            >
              {isNewCustomer ? 'Pilih dari Pelanggan Terdaftar' : '+ Tambah Pelanggan Baru'}
            </button>
          </div>

          {!isNewCustomer ? (
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Pilih Pelanggan <span className="text-rose-500">*</span>
              </label>
              <select
                required
                value={selectedCustomerId}
                onChange={(e) => setSelectedCustomerId(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
              >
                <option value="">-- Pilih Nama Pelanggan / WhatsApp --</option>
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.full_name} ({c.phone_e164})
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nama Lengkap <span className="text-rose-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={newCustomerName}
                  onChange={(e) => setNewCustomerName(e.target.value)}
                  placeholder="Contoh: Pak Budi"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nomor WhatsApp <span className="text-rose-500">*</span>
                </label>
                <input
                  type="tel"
                  required
                  value={newCustomerPhone}
                  onChange={(e) => setNewCustomerPhone(e.target.value)}
                  placeholder="0812..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
                />
              </div>
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Alamat Pelanggan (Opsional)
                </label>
                <input
                  type="text"
                  value={newCustomerAddress}
                  onChange={(e) => setNewCustomerAddress(e.target.value)}
                  placeholder="Untuk keperluan antar-jemput..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
                />
              </div>
            </div>
          )}
        </div>

        {/* Section 2: Items & Pricing Engine */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <ShoppingBag className="w-4 h-4 text-teal-700" />
              <span>Rincian Layanan Cucian</span>
            </h3>
            <button
              type="button"
              onClick={handleAddItem}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-teal-700 hover:text-teal-800 hover:bg-teal-50 rounded-xl min-h-[44px] transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Tambah Item</span>
            </button>
          </div>

          <div className="space-y-3">
            {orderItems.map((item, idx) => {
              const preview = calculateItemPreview(item.serviceId, item.quantity);
              return (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl border border-slate-200/80 bg-slate-50/50 space-y-2"
                >
                  <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                    <div className="flex-1">
                      <select
                        value={item.serviceId}
                        onChange={(e) => handleItemChange(idx, 'serviceId', e.target.value)}
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm min-h-[44px]"
                      >
                        {services.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.name} ({formatRupiah(s.unit_price)}/{s.unit})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="w-full sm:w-36 flex items-center gap-2">
                      <input
                        type="number"
                        step="0.05"
                        min="0.1"
                        required
                        value={item.quantity}
                        onChange={(e) => handleItemChange(idx, 'quantity', e.target.value)}
                        placeholder="Berat/Jml"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-center font-mono min-h-[44px]"
                      />
                    </div>

                    <div className="text-right sm:w-32 flex items-center justify-between sm:justify-end gap-3">
                      <span className="font-bold text-slate-900 text-sm">
                        {formatRupiah(preview.lineTotal)}
                      </span>
                      {orderItems.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveItem(idx)}
                          className="text-slate-400 hover:text-rose-600 p-2 rounded-lg"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>

                  {preview.note && (
                    <div className="text-[11px] font-medium text-amber-700 flex items-center gap-1.5 pl-1">
                      <Info className="w-3.5 h-3.5 text-amber-600" />
                      <span>{preview.note}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Section 3: Delivery & Additional Fees */}
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 pb-2 border-b border-slate-100">
            <Truck className="w-4 h-4 text-teal-700" />
            <span>Metode Penyerahan & Biaya Tambahan</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Metode Penerimaan Cucian
              </label>
              <select
                value={intakeMethod}
                onChange={(e) => setIntakeMethod(e.target.value as IntakeMethod)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              >
                <option value="DROP_OFF">Pelanggan Antar Sendiri (Drop-off)</option>
                <option value="COURIER_PICKUP">Dijemput Kurir Laundry</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Metode Pengambilan Cucian
              </label>
              <select
                value={returnMethod}
                onChange={(e) => setReturnMethod(e.target.value as ReturnMethod)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              >
                <option value="SELF_PICKUP">Ambil Mandiri di Kasir</option>
                <option value="HOME_DELIVERY">Diantar ke Rumah Pelanggan</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Biaya Tambahan / Express (Rp)
              </label>
              <input
                type="number"
                min={0}
                step={1000}
                value={extraCharge}
                onChange={(e) => setExtraCharge(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Biaya Ongkir / Antar (Rp)
              </label>
              <input
                type="number"
                min={0}
                step={1000}
                value={deliveryFee}
                onChange={(e) => setDeliveryFee(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Catatan Pelanggan (tertera di nota)
              </label>
              <input
                type="text"
                value={customerNotes}
                onChange={(e) => setCustomerNotes(e.target.value)}
                placeholder="Contoh: Pisahkan kelunturan, pewangi lavender"
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Catatan Internal (rahasia staf)
              </label>
              <input
                type="text"
                value={internalNotes}
                onChange={(e) => setInternalNotes(e.target.value)}
                placeholder="Contoh: Ada noda oli di bagian kerah sebelum dicuci"
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm min-h-[44px]"
              />
            </div>
          </div>
        </div>

        {/* Section 4: Summary & Submit */}
        <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-md flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="w-full sm:w-auto space-y-1">
            <div className="text-xs text-slate-400">Total Tagihan (Backend Calculated):</div>
            <div className="text-3xl font-black text-white tracking-tight">
              {formatRupiah(grandTotal)}
            </div>
            <div className="text-xs text-slate-400">
              Subtotal: {formatRupiah(subtotal)} | Biaya Tambahan: {formatRupiah(extraCharge)} | Ongkir: {formatRupiah(deliveryFee)}
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting || grandTotal <= 0}
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-teal-600 hover:bg-teal-500 font-bold text-sm tracking-wide transition-colors min-h-[48px] flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isSubmitting ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Check className="w-5 h-5" />
            )}
            <span>Simpan & Buat Nota</span>
          </button>
        </div>
      </form>
    </div>
  );
};
