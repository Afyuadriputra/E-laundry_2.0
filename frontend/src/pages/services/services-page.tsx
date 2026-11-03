import React, { useEffect, useState } from 'react';
import type { LaundryService, PricingType, ServiceCreateInput, ServiceUnit } from '../../types/services';
import { apiClient, type ApiResponse } from '../../lib/api-client';
import { useAuth } from '../../context/use-auth';
import {
  Sparkles,
  Plus,
  Clock,
  Shirt,
  Flame,
  Loader2,
  AlertCircle,
  X,
  Edit2,
  CheckCircle,
  XCircle,
} from 'lucide-react';

export const ServicesPage: React.FC = () => {
  const { user } = useAuth();
  const isOwner = user?.role === 'OWNER';

  const [services, setServices] = useState<LaundryService[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingService, setEditingService] = useState<LaundryService | null>(null);
  const [formData, setFormData] = useState<ServiceCreateInput>({
    name: '',
    pricing_type: 'PER_KG',
    unit: 'KG',
    unit_price: 10000,
    estimated_hours: 24,
    requires_ironing: true,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const fetchServices = async () => {
    try {
      const res = await apiClient<ApiResponse<LaundryService[]>>('/services');
      setServices(res.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Gagal memuat katalog layanan');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const res = await apiClient<ApiResponse<LaundryService[]>>('/services');
        if (!ignore) {
          setServices(res.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : 'Gagal memuat katalog layanan');
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

  const handleOpenCreateModal = () => {
    setEditingService(null);
    setFormData({
      name: '',
      pricing_type: 'PER_KG',
      unit: 'KG',
      unit_price: 10000,
      estimated_hours: 24,
      requires_ironing: true,
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (s: LaundryService) => {
    setEditingService(s);
    setFormData({
      name: s.name,
      pricing_type: s.pricing_type,
      unit: s.unit,
      unit_price: s.unit_price,
      estimated_hours: s.estimated_hours || 24,
      requires_ironing: s.requires_ironing,
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setIsSubmitting(true);

    try {
      if (editingService) {
        await apiClient<ApiResponse<LaundryService>>(`/services/${editingService.id}`, {
          method: 'PUT',
          body: JSON.stringify(formData),
        });
      } else {
        await apiClient<ApiResponse<LaundryService>>('/services', {
          method: 'POST',
          body: JSON.stringify(formData),
        });
      }
      setIsModalOpen(false);
      fetchServices();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Gagal menyimpan layanan');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatRupiah = (val: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(val);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-teal-700" />
            <span>Katalog Layanan & Tarif</span>
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Daftar paket cuci kiloan dan satuan. Perubahan harga otomatis membuat versi baru tanpa mengubah nota lama.
          </p>
        </div>
        {isOwner && (
          <button
            onClick={handleOpenCreateModal}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-sm transition-colors shadow-sm min-h-[44px]"
          >
            <Plus className="w-4 h-4" />
            <span>Tambah Layanan</span>
          </button>
        )}
      </div>

      {/* Error State */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Services Grid */}
      {isLoading ? (
        <div className="p-12 text-center">
          <Loader2 className="w-8 h-8 animate-spin text-teal-700 mx-auto mb-2" />
          <p className="text-sm text-slate-500">Memuat katalog...</p>
        </div>
      ) : services.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <Shirt className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-900">Belum ada layanan terdaftar</h3>
          <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
            {isOwner ? 'Klik tombol di atas untuk mendaftarkan layanan laundry pertama Anda.' : 'Hubungi Owner untuk mendaftarkan layanan.'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {services.map((s) => (
            <div
              key={s.id}
              className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-teal-300 transition-colors flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="font-bold text-slate-900 text-base leading-snug">{s.name}</h3>
                  <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                    v{s.version}
                  </span>
                </div>

                <div className="text-2xl font-black text-teal-800 tracking-tight my-2">
                  {formatRupiah(s.unit_price)}
                  <span className="text-xs font-semibold text-slate-400 font-normal"> / {s.unit}</span>
                </div>

                <div className="flex flex-wrap gap-1.5 my-3">
                  <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-100">
                    {s.pricing_type === 'PER_KG' ? 'Kiloan' : 'Satuan'}
                  </span>
                  {s.requires_ironing ? (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-100">
                      <Flame className="w-3 h-3" /> Termasuk Setrika
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-600">
                      Cuci Kering
                    </span>
                  )}
                  {s.estimated_hours && (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-600">
                      <Clock className="w-3 h-3 text-slate-400" /> {s.estimated_hours} Jam
                    </span>
                  )}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-400 flex items-center gap-1">
                  {s.is_active ? (
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-slate-400" />
                  )}
                  <span>{s.is_active ? 'Aktif' : 'Nonaktif'}</span>
                </span>
                {isOwner && (
                  <button
                    onClick={() => handleOpenEditModal(s)}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-teal-700 hover:text-teal-800 p-1.5 rounded-lg hover:bg-teal-50 min-h-[36px]"
                  >
                    <Edit2 className="w-3.5 h-3.5" />
                    <span>Ubah Tarif</span>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal Create/Edit */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">
                {editingService ? 'Ubah Layanan & Tarif' : 'Tambah Layanan Baru'}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {formError && (
              <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{formError}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Nama Layanan <span className="text-rose-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Contoh: Cuci Setrika Reguler"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Metode Tarif
                  </label>
                  <select
                    value={formData.pricing_type}
                    onChange={(e) => {
                      const pt = e.target.value as PricingType;
                      setFormData({
                        ...formData,
                        pricing_type: pt,
                        unit: pt === 'PER_KG' ? 'KG' : 'PCS',
                      });
                    }}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
                  >
                    <option value="PER_KG">Kiloan (PER_KG)</option>
                    <option value="PER_ITEM">Satuan (PER_ITEM)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Satuan</label>
                  <select
                    value={formData.unit}
                    onChange={(e) => setFormData({ ...formData, unit: e.target.value as ServiceUnit })}
                    className="w-full px-3 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
                  >
                    <option value="KG">Kilogram (KG)</option>
                    <option value="PCS">Potong/Pcs (PCS)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Tarif (Rp) <span className="text-rose-500">*</span>
                  </label>
                  <input
                    type="number"
                    required
                    min={0}
                    step={500}
                    value={formData.unit_price}
                    onChange={(e) => setFormData({ ...formData, unit_price: parseInt(e.target.value) || 0 })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Estimasi Jam</label>
                  <input
                    type="number"
                    min={1}
                    value={formData.estimated_hours || 24}
                    onChange={(e) => setFormData({ ...formData, estimated_hours: parseInt(e.target.value) || 24 })}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
                  />
                </div>
              </div>

              <div className="pt-1">
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={formData.requires_ironing}
                    onChange={(e) => setFormData({ ...formData, requires_ironing: e.target.checked })}
                    className="w-4 h-4 rounded text-teal-700 focus:ring-teal-700 border-slate-300"
                  />
                  <span className="text-xs font-medium text-slate-700">
                    Mencakup proses setrika pakaian (Tahap IRONING aktif)
                  </span>
                </label>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2.5 rounded-xl text-slate-600 hover:bg-slate-100 text-sm font-semibold min-h-[44px]"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-5 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white text-sm font-semibold min-h-[44px] flex items-center gap-2 disabled:opacity-50"
                >
                  {isSubmitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  <span>{editingService ? 'Simpan Perubahan' : 'Tambah Layanan'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
