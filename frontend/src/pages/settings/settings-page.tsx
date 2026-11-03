import React, { useEffect, useState } from 'react';
import { apiClient, ApiError, type ApiResponse } from '../../lib/api-client';
import type { BusinessProfile } from '../../types/auth';
import {
  AlertCircle,
  Building2,
  CheckCircle2,
  Clock,
  Coins,
  Loader2,
  Scale,
  Save,
  Truck,
} from 'lucide-react';

interface BusinessSettingsData {
  pickup_enabled: boolean;
  delivery_enabled: boolean;
  default_delivery_fee: number;
  default_completion_hours: number;
  weight_precision: number;
  weight_rounding_mode: string;
}

export const SettingsPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Form states
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [deliveryFee, setDeliveryFee] = useState(5000);
  const [completionHours, setCompletionHours] = useState(48);
  const [pickupEnabled, setPickupEnabled] = useState(true);
  const [deliveryEnabled, setDeliveryEnabled] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const [profileRes, settingsRes] = await Promise.all([
        apiClient<ApiResponse<BusinessProfile>>('/business'),
        apiClient<ApiResponse<BusinessSettingsData>>('/settings'),
      ]);

      setName(profileRes.data.name);
      setPhone(profileRes.data.phone_e164);
      setAddress(profileRes.data.address);

      setDeliveryFee(settingsRes.data.default_delivery_fee);
      setCompletionHours(settingsRes.data.default_completion_hours);
      setPickupEnabled(settingsRes.data.pickup_enabled);
      setDeliveryEnabled(settingsRes.data.delivery_enabled);
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal memuat pengaturan.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const [profileRes, settingsRes] = await Promise.all([
          apiClient<ApiResponse<BusinessProfile>>('/business'),
          apiClient<ApiResponse<BusinessSettingsData>>('/settings'),
        ]);

        if (!ignore) {
          setName(profileRes.data.name);
          setPhone(profileRes.data.phone_e164);
          setAddress(profileRes.data.address);

          setDeliveryFee(settingsRes.data.default_delivery_fee);
          setCompletionHours(settingsRes.data.default_completion_hours);
          setPickupEnabled(settingsRes.data.pickup_enabled);
          setDeliveryEnabled(settingsRes.data.delivery_enabled);
        }
      } catch (err) {
        if (!ignore) {
          if (err instanceof ApiError) {
            setErrorMsg(err.message);
          } else {
            setErrorMsg('Gagal memuat pengaturan.');
          }
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
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      await Promise.all([
        apiClient<ApiResponse<BusinessProfile>>('/business', {
          method: 'PATCH',
          body: JSON.stringify({
            name: name.trim(),
            phone_e164: phone.trim(),
            address: address.trim(),
          }),
        }),
        apiClient<ApiResponse<BusinessSettingsData>>('/settings', {
          method: 'PATCH',
          body: JSON.stringify({
            default_delivery_fee: Number(deliveryFee),
            default_completion_hours: Number(completionHours),
            pickup_enabled: pickupEnabled,
            delivery_enabled: deliveryEnabled,
          }),
        }),
      ]);
      setSuccessMsg('Pengaturan usaha berhasil diperbarui.');
      await fetchData();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal menyimpan perubahan pengaturan.');
      }
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
        <Loader2 className="w-8 h-8 animate-spin text-teal-700 mx-auto mb-3" />
        <p className="text-sm text-slate-500 font-medium">Memuat pengaturan usaha...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Pengaturan Usaha</h1>
        <p className="text-sm text-slate-500 mt-1">
          Konfigurasi profil laundry, kebijakan tarif antar-jemput, dan estimasi waktu
        </p>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>{errorMsg}</div>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-start gap-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div>{successMsg}</div>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100 text-slate-900 font-semibold text-base">
            <Building2 className="w-5 h-5 text-teal-700" />
            <span>Identitas Usaha</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                Nama Laundry
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                No. WhatsApp Resmi Usaha
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                Alamat Lengkap Workshop / Outlet
              </label>
              <textarea
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                rows={3}
                required
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Operational & Delivery Settings */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100 text-slate-900 font-semibold text-base">
            <Truck className="w-5 h-5 text-teal-700" />
            <span>Operasional & Antar-Jemput</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5 flex items-center gap-1.5">
                <Coins className="w-4 h-4 text-slate-500" />
                <span>Tarif Standar Delivery (Rp)</span>
              </label>
              <input
                type="number"
                min={0}
                step={500}
                value={deliveryFee}
                onChange={(e) => setDeliveryFee(Number(e.target.value))}
                required
                className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
              />
              <p className="text-xs text-slate-400 mt-1">Tarif tetap (flat fee) per pengiriman.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5 flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-slate-500" />
                <span>Estimasi Selesai Standar (Jam)</span>
              </label>
              <input
                type="number"
                min={1}
                value={completionHours}
                onChange={(e) => setCompletionHours(Number(e.target.value))}
                required
                className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
              />
              <p className="text-xs text-slate-400 mt-1">Misal: 48 jam (2 hari kerja standar).</p>
            </div>

            <div className="flex items-center gap-3 pt-2">
              <input
                type="checkbox"
                id="pickup_enabled"
                checked={pickupEnabled}
                onChange={(e) => setPickupEnabled(e.target.checked)}
                className="w-5 h-5 rounded text-teal-700 focus:ring-teal-700 border-slate-300"
              />
              <label htmlFor="pickup_enabled" className="text-sm font-medium text-slate-800">
                Aktifkan Layanan Penjemputan (Pickup)
              </label>
            </div>

            <div className="flex items-center gap-3 pt-2">
              <input
                type="checkbox"
                id="delivery_enabled"
                checked={deliveryEnabled}
                onChange={(e) => setDeliveryEnabled(e.target.checked)}
                className="w-5 h-5 rounded text-teal-700 focus:ring-teal-700 border-slate-300"
              />
              <label htmlFor="delivery_enabled" className="text-sm font-medium text-slate-800">
                Aktifkan Layanan Pengantaran (Delivery)
              </label>
            </div>
          </div>
        </div>

        {/* Invariant Rules Display */}
        <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5 space-y-2">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-600">
            <Scale className="w-4 h-4 text-slate-500" />
            <span>Kebijakan Presisi Timbangan (DEC-01 & DEC-02)</span>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Sistem menggunakan pembulatan kelipatan 0.1 kg dengan mode HALF_UP dan batas minimal kiloan 3.0 kg sesuai spesifikasi resmi.
          </p>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-medium text-sm shadow-sm min-h-[44px] disabled:opacity-50 transition-colors"
          >
            {isSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            <span>Simpan Perubahan</span>
          </button>
        </div>
      </form>
    </div>
  );
};
