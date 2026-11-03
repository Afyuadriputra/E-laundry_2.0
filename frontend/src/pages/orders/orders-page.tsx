import React, { useEffect, useState } from 'react';
import type { OrderListItem, OperationalStatus } from '../../types/orders';
import { apiClient, type ApiResponse } from '../../lib/api-client';
import { useAuth } from '../../context/use-auth';
import { CreateOrderPage } from './create-order-page';
import { OrderDetailPage } from './order-detail-page';
import {
  ShoppingBag,
  Plus,
  Search,
  Clock,
  Calendar,
  ChevronRight,
  Loader2,
  AlertCircle,
} from 'lucide-react';

export const OrdersPage: React.FC = () => {
  const { user } = useAuth();
  const isCashierOrOwner = user?.role === 'OWNER' || user?.role === 'CASHIER';

  const [view, setView] = useState<'list' | 'create' | 'detail'>('list');
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);

  const [orders, setOrders] = useState<OrderListItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  const fetchOrders = async (query = '', status = '') => {
    setIsLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (query) params.append('search', query);
      if (status) params.append('operational_status', status);

      const queryString = params.toString();
      const endpoint = queryString ? `/orders?${queryString}` : '/orders';
      const res = await apiClient<ApiResponse<OrderListItem[]>>(endpoint);
      setOrders(res.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Gagal memuat daftar pesanan');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (view === 'list') {
      const timer = setTimeout(() => {
        fetchOrders(search, statusFilter);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [search, statusFilter, view]);

  const formatRupiah = (val: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(val);
  };

  const getStatusBadge = (status: OperationalStatus) => {
    switch (status) {
      case 'RECEIVED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-800">Diterima</span>;
      case 'QUEUED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-800 border border-blue-200">Antrean</span>;
      case 'WASHING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-50 text-cyan-800 border border-cyan-200">Cuci</span>;
      case 'DRYING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-sky-50 text-sky-800 border border-sky-200">Kering</span>;
      case 'IRONING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">Setrika</span>;
      case 'QC_PACKING':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-purple-50 text-purple-800 border border-purple-200">QC/Packing</span>;
      case 'READY':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">Siap Ambil</span>;
      case 'COMPLETED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-600 text-white">Selesai</span>;
      case 'CANCELLED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800">Batal</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-700">{status}</span>;
    }
  };

  if (view === 'create') {
    return (
      <CreateOrderPage
        onBack={() => setView('list')}
        onSuccess={(id) => {
          setSelectedOrderId(id);
          setView('detail');
        }}
      />
    );
  }

  if (view === 'detail' && selectedOrderId) {
    return (
      <OrderDetailPage
        orderId={selectedOrderId}
        onBack={() => {
          setSelectedOrderId(null);
          setView('list');
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ShoppingBag className="w-6 h-6 text-teal-700" />
            <span>Manajemen Pesanan Laundry</span>
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Pantau dan perbarui tahapan pencucian pelanggan secara real-time.
          </p>
        </div>

        {isCashierOrOwner && (
          <button
            onClick={() => setView('create')}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-semibold text-sm transition-colors shadow-sm min-h-[44px]"
          >
            <Plus className="w-4 h-4" />
            <span>Buat Pesanan Baru</span>
          </button>
        )}
      </div>

      {/* Filter Tabs & Search Bar */}
      <div className="space-y-3">
        <div className="relative">
          <Search className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Cari nomor nota atau nama/telepon pelanggan..."
            className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-slate-200 bg-white text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-700/20 focus:border-teal-700 min-h-[44px]"
          />
        </div>

        {/* Status Filter Scrollable Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none text-xs">
          {[
            { label: 'Semua Status', value: '' },
            { label: 'Diterima Kasir', value: 'RECEIVED' },
            { label: 'Dalam Antrean', value: 'QUEUED' },
            { label: 'Pencucian', value: 'WASHING' },
            { label: 'Pengeringan', value: 'DRYING' },
            { label: 'Penyetrikaan', value: 'IRONING' },
            { label: 'QC & Packing', value: 'QC_PACKING' },
            { label: 'Siap Ambil', value: 'READY' },
            { label: 'Selesai', value: 'COMPLETED' },
            { label: 'Dibatalkan', value: 'CANCELLED' },
          ].map((tab) => (
            <button
              key={tab.value}
              onClick={() => setStatusFilter(tab.value)}
              className={`px-3 py-1.5 rounded-full font-medium whitespace-nowrap transition-colors min-h-[36px] ${
                statusFilter === tab.value
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Orders List */}
      {isLoading ? (
        <div className="p-12 text-center">
          <Loader2 className="w-8 h-8 animate-spin text-teal-700 mx-auto mb-2" />
          <p className="text-sm text-slate-500">Memuat pesanan...</p>
        </div>
      ) : orders.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <ShoppingBag className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-900">Tidak ada pesanan ditemukan</h3>
          <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
            {search || statusFilter ? 'Coba ubah kata kunci atau filter status.' : 'Mulai dengan membuat nota pesanan pertama.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {orders.map((o) => (
            <div
              key={o.id}
              onClick={() => {
                setSelectedOrderId(o.id);
                setView('detail');
              }}
              className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:border-teal-400 hover:shadow-sm transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-2.5 flex-wrap">
                  <span className="font-mono font-bold text-slate-900 text-sm">{o.order_number}</span>
                  {getStatusBadge(o.operational_status)}
                  <span className="text-[11px] font-semibold text-slate-400">v{o.version}</span>
                </div>

                <div className="text-sm font-semibold text-slate-800 flex items-center gap-2">
                  <span>{o.customer_name}</span>
                  <span className="text-xs font-normal text-slate-400 font-mono">({o.customer_phone})</span>
                </div>

                <div className="flex items-center gap-4 text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    <span>{new Date(o.created_at).toLocaleDateString('id-ID')}</span>
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>Estimasi: {new Date(o.estimated_completion_at).toLocaleDateString('id-ID')}</span>
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between sm:justify-end gap-4 pt-3 sm:pt-0 border-t sm:border-0 border-slate-100">
                <div className="text-left sm:text-right">
                  <div className="text-xs text-slate-400">Total Tagihan:</div>
                  <div className="text-base font-black text-teal-800 font-mono">
                    {formatRupiah(o.total_amount)}
                  </div>
                </div>
                <div className="p-2 rounded-xl bg-slate-50 text-slate-400 group-hover:text-teal-700">
                  <ChevronRight className="w-5 h-5" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
