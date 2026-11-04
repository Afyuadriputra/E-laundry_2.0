import React, { useCallback, useEffect, useState } from 'react';
import { useAuth } from '../../context/use-auth';
import { reportsApi } from '../../services/reports';
import type {
  FinancialReportSummary,
  OrdersReportSummary,
  OutstandingBalanceItem,
} from '../../types/reports';
import {
  FileText,
  DollarSign,
  AlertTriangle,
  Download,
  RefreshCw,
  Phone,
  AlertCircle,
  X,
  TrendingUp,
  CreditCard,
  ShoppingBag,
} from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const { user } = useAuth();
  const isOwner = user?.role === 'OWNER';

  // Sub-tabs: 'orders' | 'finances' | 'outstanding'
  const [activeTab, setActiveTab] = useState<'orders' | 'finances' | 'outstanding'>(
    isOwner ? 'finances' : 'orders'
  );

  // Date range filter ('today' | '7days' | '30days')
  const [dateRange, setDateRange] = useState<'today' | '7days' | '30days'>('today');

  // Reports state
  const [ordersSummary, setOrdersSummary] = useState<OrdersReportSummary | null>(null);
  const [financialSummary, setFinancialSummary] = useState<FinancialReportSummary | null>(null);
  const [outstandingList, setOutstandingList] = useState<OutstandingBalanceItem[]>([]);

  // Filter state for orders
  const [orderStatusFilter, setOrderStatusFilter] = useState('');
  const [paymentStatusFilter, setPaymentStatusFilter] = useState('');

  // UI state
  const [isLoading, setIsLoading] = useState(true);
  const [isExporting, setIsExporting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Compute date strings from preset
  const getDateBounds = useCallback(() => {
    const today = new Date();
    const endStr = today.toISOString().split('T')[0];
    const start = new Date();

    if (dateRange === '7days') {
      start.setDate(today.getDate() - 7);
    } else if (dateRange === '30days') {
      start.setDate(today.getDate() - 30);
    }
    const startStr = start.toISOString().split('T')[0];
    return { startStr, endStr };
  }, [dateRange]);

  const loadReportData = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const { startStr, endStr } = getDateBounds();

      if (activeTab === 'finances' && isOwner) {
        const finData = await reportsApi.getFinancialReport({
          start_date: startStr,
          end_date: endStr,
        });
        setFinancialSummary(finData);
      } else if (activeTab === 'orders') {
        const ordData = await reportsApi.getOrdersReport({
          start_date: startStr,
          end_date: endStr,
          operational_status: orderStatusFilter || undefined,
          payment_status: paymentStatusFilter || undefined,
        });
        setOrdersSummary(ordData);
      } else if (activeTab === 'outstanding') {
        const outData = await reportsApi.getOutstandingReport();
        setOutstandingList(outData);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal memuat laporan data.';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  }, [activeTab, isOwner, getDateBounds, orderStatusFilter, paymentStatusFilter]);

  useEffect(() => {
    let ignore = false;
    async function fetchData() {
      try {
        const { startStr, endStr } = getDateBounds();
        if (activeTab === 'finances' && isOwner) {
          const finData = await reportsApi.getFinancialReport({
            start_date: startStr,
            end_date: endStr,
          });
          if (!ignore) setFinancialSummary(finData);
        } else if (activeTab === 'orders') {
          const ordData = await reportsApi.getOrdersReport({
            start_date: startStr,
            end_date: endStr,
            operational_status: orderStatusFilter || undefined,
            payment_status: paymentStatusFilter || undefined,
          });
          if (!ignore) setOrdersSummary(ordData);
        } else if (activeTab === 'outstanding') {
          const outData = await reportsApi.getOutstandingReport();
          if (!ignore) setOutstandingList(outData);
        }
      } catch (err: unknown) {
        if (!ignore) {
          const msg = err instanceof Error ? err.message : 'Gagal memuat laporan data.';
          setErrorMsg(msg);
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }
    fetchData();
    return () => {
      ignore = true;
    };
  }, [activeTab, isOwner, getDateBounds, orderStatusFilter, paymentStatusFilter]);

  // Handle CSV exports
  const handleExport = async (type: 'orders' | 'payments' | 'expenses') => {
    setIsExporting(true);
    setErrorMsg(null);
    try {
      const { startStr, endStr } = getDateBounds();
      let endpoint = '';
      let filename = '';

      if (type === 'orders') {
        endpoint = `/reports/export/orders.csv?start_date=${startStr}&end_date=${endStr}`;
        filename = `laporan_pesanan_${startStr}_sd_${endStr}.csv`;
      } else if (type === 'payments') {
        endpoint = `/reports/export/payments.csv?start_date=${startStr}&end_date=${endStr}`;
        filename = `laporan_pembayaran_${startStr}_sd_${endStr}.csv`;
      } else if (type === 'expenses') {
        endpoint = `/reports/export/expenses.csv?start_date=${startStr}&end_date=${endStr}`;
        filename = `laporan_pengeluaran_${startStr}_sd_${endStr}.csv`;
      }

      await reportsApi.downloadCsv(endpoint, filename);
      setSuccessMsg(`File CSV ${filename} berhasil diunduh.`);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal mengunduh file CSV.';
      setErrorMsg(msg);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 mb-2">
            <FileText className="w-3.5 h-3.5" />
            <span>Laporan & Pembukuan Operasional (M6)</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Pusat Laporan & Rekonsiliasi
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Analisis kinerja pesanan, arus kas transaksi terverifikasi, dan tagihan belum lunas.
          </p>
        </div>

        {/* Global Date Preset & Refresh */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex bg-slate-100 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setDateRange('today')}
              className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                dateRange === 'today' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Hari Ini
            </button>
            <button
              onClick={() => setDateRange('7days')}
              className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                dateRange === '7days' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              7 Hari
            </button>
            <button
              onClick={() => setDateRange('30days')}
              className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                dateRange === '30days' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              30 Hari
            </button>
          </div>

          <button
            onClick={loadReportData}
            disabled={isLoading}
            className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 min-h-[44px] transition-colors cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Segarkan</span>
          </button>
        </div>
      </div>

      {/* Notifications */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">{errorMsg}</div>
          <button onClick={() => setErrorMsg(null)} className="text-rose-500 hover:text-rose-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm flex items-start gap-2.5">
          <TrendingUp className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div className="flex-1">{successMsg}</div>
          <button onClick={() => setSuccessMsg(null)} className="text-emerald-500 hover:text-emerald-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Navigation Sub-Tabs */}
      <div className="border-b border-slate-200">
        <nav className="flex gap-4">
          {isOwner && (
            <button
              onClick={() => setActiveTab('finances')}
              className={`pb-3 text-sm font-bold border-b-2 transition-colors cursor-pointer ${
                activeTab === 'finances'
                  ? 'border-teal-700 text-teal-800'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              Ringkasan Finansial
            </button>
          )}
          <button
            onClick={() => setActiveTab('orders')}
            className={`pb-3 text-sm font-bold border-b-2 transition-colors cursor-pointer ${
              activeTab === 'orders'
                ? 'border-teal-700 text-teal-800'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Laporan Pesanan
          </button>
          <button
            onClick={() => setActiveTab('outstanding')}
            className={`pb-3 text-sm font-bold border-b-2 transition-colors cursor-pointer ${
              activeTab === 'outstanding'
                ? 'border-teal-700 text-teal-800'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Tagihan Belum Lunas (Piutang)
          </button>
        </nav>
      </div>

      {/* ============================================================== */}
      {/* TAB 1: FINANCIAL SUMMARY (OWNER ONLY) */}
      {/* ============================================================== */}
      {activeTab === 'finances' && isOwner && (
        <div className="space-y-6">
          {financialSummary && (
            <>
              {/* Financial KPI Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between text-slate-500 mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider">Uang Masuk Diterima</span>
                    <DollarSign className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div className="text-xl font-bold text-slate-900">
                    Rp {financialSummary.total_cash_received.toLocaleString('id-ID')}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">Pembayaran sah (tidak termasuk void)</p>
                </div>

                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between text-slate-500 mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider">Total Pengeluaran</span>
                    <CreditCard className="w-5 h-5 text-rose-600" />
                  </div>
                  <div className="text-xl font-bold text-slate-900">
                    Rp {financialSummary.total_expenses.toLocaleString('id-ID')}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">Biaya operasional & bahan</p>
                </div>

                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between text-slate-500 mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider">Selisih Kas Bersih</span>
                    <TrendingUp className="w-5 h-5 text-teal-600" />
                  </div>
                  <div
                    className={`text-xl font-bold ${
                      financialSummary.simple_cash_difference >= 0 ? 'text-teal-700' : 'text-rose-700'
                    }`}
                  >
                    Rp {financialSummary.simple_cash_difference.toLocaleString('id-ID')}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">Uang Masuk - Pengeluaran</p>
                </div>

                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
                  <div className="flex items-center justify-between text-slate-500 mb-2">
                    <span className="text-xs font-semibold uppercase tracking-wider">Piutang Belum Lunas</span>
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                  </div>
                  <div className="text-xl font-bold text-amber-700">
                    Rp {financialSummary.outstanding_receivables.toLocaleString('id-ID')}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">Sisa tagihan seluruh pesanan aktif</p>
                </div>
              </div>

              {/* Breakdown Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Method Breakdown */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-slate-900">Penerimaan per Metode Bayar</h3>
                    <button
                      onClick={() => handleExport('payments')}
                      disabled={isExporting}
                      className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 min-h-[44px] transition-colors cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Unduh CSV Pembayaran</span>
                    </button>
                  </div>
                  <div className="space-y-2">
                    {Object.entries(financialSummary.cash_by_method).map(([method, amt]) => (
                      <div key={method} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 text-xs">
                        <span className="font-bold text-slate-700">{method}</span>
                        <span className="font-mono font-bold text-slate-900">Rp {amt.toLocaleString('id-ID')}</span>
                      </div>
                    ))}
                    {Object.keys(financialSummary.cash_by_method).length === 0 && (
                      <p className="text-xs text-slate-400 text-center py-4">Belum ada pembayaran pada periode ini.</p>
                    )}
                  </div>
                </div>

                {/* Expense Breakdown */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-slate-900">Pengeluaran per Kategori</h3>
                    <button
                      onClick={() => handleExport('expenses')}
                      disabled={isExporting}
                      className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 min-h-[44px] transition-colors cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Unduh CSV Pengeluaran</span>
                    </button>
                  </div>
                  <div className="space-y-2">
                    {Object.entries(financialSummary.expenses_by_category).map(([cat, amt]) => (
                      <div key={cat} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 text-xs">
                        <span className="font-bold text-slate-700">{cat}</span>
                        <span className="font-mono font-bold text-rose-700">Rp {amt.toLocaleString('id-ID')}</span>
                      </div>
                    ))}
                    {Object.keys(financialSummary.expenses_by_category).length === 0 && (
                      <p className="text-xs text-slate-400 text-center py-4">Belum ada pengeluaran pada periode ini.</p>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 2: ORDERS REPORT */}
      {/* ============================================================== */}
      {activeTab === 'orders' && (
        <div className="space-y-4">
          {/* Filters Bar */}
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-3 text-xs">
              <div>
                <span className="font-semibold text-slate-500 mr-2">Status Operasional:</span>
                <select
                  value={orderStatusFilter}
                  onChange={(e) => setOrderStatusFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-800 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                >
                  <option value="">Semua Status</option>
                  <option value="RECEIVED">Diterima (RECEIVED)</option>
                  <option value="WASHING">Pencucian (WASHING)</option>
                  <option value="DRYING">Pengeringan (DRYING)</option>
                  <option value="IRONING">Setrika (IRONING)</option>
                  <option value="READY">Siap (READY)</option>
                  <option value="COMPLETED">Selesai (COMPLETED)</option>
                  <option value="CANCELLED">Dibatalkan</option>
                </select>
              </div>

              <div>
                <span className="font-semibold text-slate-500 mr-2">Status Pembayaran:</span>
                <select
                  value={paymentStatusFilter}
                  onChange={(e) => setPaymentStatusFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-800 text-xs focus:ring-2 focus:ring-teal-500 focus:outline-hidden"
                >
                  <option value="">Semua Pembayaran</option>
                  <option value="PAID">Lunas (PAID)</option>
                  <option value="PARTIALLY_PAID">Sebagian (PARTIALLY_PAID)</option>
                  <option value="UNPAID">Belum Bayar (UNPAID)</option>
                </select>
              </div>
            </div>

            <button
              onClick={() => handleExport('orders')}
              disabled={isExporting}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-teal-800 bg-teal-50 hover:bg-teal-100 border border-teal-200 transition-colors cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Unduh CSV Pesanan</span>
            </button>
          </div>

          {/* Aggregated Totals Banner */}
          {ordersSummary && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
                <span className="text-slate-500">Jumlah Pesanan</span>
                <div className="text-base font-bold text-slate-900 mt-0.5">{ordersSummary.total_orders}</div>
              </div>
              <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
                <span className="text-slate-500">Nilai Tagihan Sah</span>
                <div className="text-base font-bold text-slate-900 mt-0.5">
                  Rp {ordersSummary.total_amount.toLocaleString('id-ID')}
                </div>
              </div>
              <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
                <span className="text-slate-500">Terbayar</span>
                <div className="text-base font-bold text-emerald-700 mt-0.5">
                  Rp {ordersSummary.total_paid.toLocaleString('id-ID')}
                </div>
              </div>
              <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-xs">
                <span className="text-slate-500">Sisa Tagihan</span>
                <div className="text-base font-bold text-amber-700 mt-0.5">
                  Rp {ordersSummary.total_outstanding.toLocaleString('id-ID')}
                </div>
              </div>
            </div>
          )}

          {/* Orders Table */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="px-4 py-3">No. Pesanan</th>
                    <th className="px-4 py-3">Pelanggan</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Total Tagihan</th>
                    <th className="px-4 py-3">Dibayar</th>
                    <th className="px-4 py-3">Sisa</th>
                    <th className="px-4 py-3">Tanggal</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {ordersSummary?.items.map((ord) => (
                    <tr key={ord.order_id} className="hover:bg-slate-50/60 transition-colors">
                      <td className="px-4 py-3 font-mono font-bold text-slate-900">{ord.order_number}</td>
                      <td className="px-4 py-3">
                        <div className="font-semibold text-slate-800">{ord.customer_name}</div>
                        <div className="text-slate-400 text-[11px]">{ord.customer_phone}</div>
                      </td>
                      <td className="px-4 py-3 space-y-1">
                        <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-slate-100 text-slate-700">
                          {ord.operational_status}
                        </span>
                        <div>
                          <span
                            className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                              ord.payment_status === 'PAID'
                                ? 'bg-emerald-100 text-emerald-800'
                                : ord.payment_status === 'PARTIALLY_PAID'
                                ? 'bg-amber-100 text-amber-800'
                                : 'bg-rose-100 text-rose-800'
                            }`}
                          >
                            {ord.payment_status}
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3 font-mono font-bold text-slate-900">
                        Rp {ord.total_amount.toLocaleString('id-ID')}
                      </td>
                      <td className="px-4 py-3 font-mono text-emerald-700">
                        Rp {ord.paid_amount.toLocaleString('id-ID')}
                      </td>
                      <td className="px-4 py-3 font-mono text-amber-700">
                        Rp {ord.remaining_amount.toLocaleString('id-ID')}
                      </td>
                      <td className="px-4 py-3 text-slate-500">
                        {new Date(ord.created_at).toLocaleDateString('id-ID', {
                          day: 'numeric',
                          month: 'short',
                        })}
                      </td>
                    </tr>
                  ))}

                  {ordersSummary?.items.length === 0 && !isLoading && (
                    <tr>
                      <td colSpan={7} className="px-4 py-8 text-center text-slate-400">
                        Tidak ada pesanan yang sesuai filter.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 3: OUTSTANDING BALANCES (PIUTANG) */}
      {/* ============================================================== */}
      {activeTab === 'outstanding' && (
        <div className="space-y-4">
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Daftar Tagihan Belum Lunas</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Pesanan aktif yang masih memiliki sisa pembayaran yang harus ditagihkan ke pelanggan.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {outstandingList.map((item) => (
              <div
                key={item.order_id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="font-mono text-xs font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded-md">
                        {item.order_number}
                      </span>
                      <h4 className="text-base font-bold text-slate-900 mt-1">{item.customer_name}</h4>
                    </div>
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">
                      Sisa Rp {item.remaining_amount.toLocaleString('id-ID')}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
                    <span>Total: Rp {item.total_amount.toLocaleString('id-ID')}</span>
                    <span>Sudah Bayar: Rp {item.paid_amount.toLocaleString('id-ID')}</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-xs text-slate-400">
                    Status: <strong className="text-slate-700">{item.operational_status}</strong>
                  </span>
                  {item.customer_phone && item.customer_phone !== '-' && (
                    <a
                      href={`https://wa.me/${item.customer_phone.replace(/[^0-9]/g, '')}?text=Halo%20${encodeURIComponent(
                        item.customer_name
                      )},%20kami%20dari%20laundry%20menginformasikan%20tagihan%20pesanan%20${
                        item.order_number
                      }%20tersisa%20Rp%20${item.remaining_amount.toLocaleString('id-ID')}.%20Terima%20kasih!`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 min-h-[44px] transition-colors"
                    >
                      <Phone className="w-3.5 h-3.5" />
                      <span>Ingatkan via WA</span>
                    </a>
                  )}
                </div>
              </div>
            ))}

            {outstandingList.length === 0 && !isLoading && (
              <div className="col-span-2 p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-xs">
                <ShoppingBag className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                <h3 className="text-base font-bold text-slate-900">Semua Tagihan Telah Lunas</h3>
                <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
                  Tidak ada pesanan aktif yang memiliki sisa pembayaran saat ini.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
export default ReportsPage;
