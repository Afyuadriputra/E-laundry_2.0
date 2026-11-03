import React, { useEffect, useState } from 'react';
import { AuthProvider } from './context/auth-context';
import { useAuth } from './context/use-auth';
import { LoginPage } from './pages/login/login-page';
import { AppShell } from './components/layout/app-shell';
import { UsersPage } from './pages/users/users-page';
import { SettingsPage } from './pages/settings/settings-page';
import { CustomersPage } from './pages/customers/customers-page';
import { ServicesPage } from './pages/services/services-page';
import { OrdersPage } from './pages/orders/orders-page';
import { ExpensesPage } from './pages/expenses/expenses-page';
import { DeliveryPage } from './pages/delivery/delivery-page';
import { ReportsPage } from './pages/reports/reports-page';
import { PublicTrackingPage } from './pages/tracking/public-tracking-page';
import { reportsApi } from './services/reports';
import type { DashboardSummary, OverdueOrder } from './types/reports';
import {
  Activity,
  CheckCircle2,
  Clock,
  Loader2,
  ShieldCheck,
  TrendingUp,
  DollarSign,
  AlertTriangle,
  Package,
  CreditCard,
} from 'lucide-react';

const DashboardView: React.FC = () => {
  const { user } = useAuth();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [overdueOrders, setOverdueOrders] = useState<OverdueOrder[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;
    async function loadMetrics() {
      try {
        const [sumData, ovData] = await Promise.all([
          reportsApi.getDashboardSummary(),
          reportsApi.getOverdueOrders().catch(() => []),
        ]);
        if (!ignore) {
          setSummary(sumData);
          setOverdueOrders(ovData);
        }
      } catch (err) {
        console.error('Failed to load dashboard metrics', err);
      } finally {
        if (!ignore) setIsLoading(false);
      }
    }
    loadMetrics();
    return () => {
      ignore = true;
    };
  }, []);

  if (!user) return null;
  const isOwner = user.role === 'OWNER';

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 mb-2">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Sesi Terotentikasi</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Selamat datang, {user.full_name}
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">
            Role aktif: <strong className="text-slate-800">{user.role}</strong> di sistem operasional laundry.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-50 px-3 py-2 rounded-xl border border-slate-200/60">
          {isLoading ? (
            <Loader2 className="w-4 h-4 text-teal-600 animate-spin" />
          ) : (
            <Clock className="w-4 h-4 text-slate-400" />
          )}
          <span>Zona Waktu: Asia/Jakarta (WIB)</span>
        </div>
      </div>

      {/* Overdue Alert Banner if Any */}
      {overdueOrders.length > 0 && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 shadow-xs flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <h4 className="text-sm font-bold">Peringatan: {overdueOrders.length} Pesanan Terlambat!</h4>
            <p className="text-xs text-amber-700 mt-0.5">
              Terdapat pesanan yang telah melampaui estimasi waktu selesai. Mohon segera diprioritaskan.
            </p>
          </div>
        </div>
      )}

      {/* Financial Metrics Grid (Owner Only) */}
      {isOwner && summary?.order_value_period !== undefined && (
        <div className="space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Kinerja Finansial Hari Ini
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Uang Masuk Diterima</span>
                <DollarSign className="w-5 h-5 text-emerald-600" />
              </div>
              <div className="text-xl font-bold text-slate-900">
                Rp {(summary?.cash_received_period ?? 0).toLocaleString('id-ID')}
              </div>
              <p className="text-xs text-slate-500 mt-1">Pembayaran sah hari ini</p>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Nilai Pesanan Baru</span>
                <Activity className="w-5 h-5 text-teal-600" />
              </div>
              <div className="text-xl font-bold text-slate-900">
                Rp {(summary?.order_value_period ?? 0).toLocaleString('id-ID')}
              </div>
              <p className="text-xs text-slate-500 mt-1">Nilai bruto pesanan hari ini</p>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Pengeluaran</span>
                <CreditCard className="w-5 h-5 text-rose-600" />
              </div>
              <div className="text-xl font-bold text-slate-900">
                Rp {(summary?.expenses_period ?? 0).toLocaleString('id-ID')}
              </div>
              <p className="text-xs text-slate-500 mt-1">Biaya operasional tercatat</p>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Selisih Kas Bersih</span>
                <TrendingUp className="w-5 h-5 text-teal-600" />
              </div>
              <div
                className={`text-xl font-bold ${
                  (summary?.simple_cash_difference ?? 0) >= 0 ? 'text-teal-700' : 'text-rose-700'
                }`}
              >
                Rp {(summary?.simple_cash_difference ?? 0).toLocaleString('id-ID')}
              </div>
              <p className="text-xs text-slate-500 mt-1">Uang Masuk - Pengeluaran</p>
            </div>
          </div>
        </div>
      )}

      {/* Operational Highlights Grid */}
      <div className="space-y-2">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Operasional Hari Ini
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Pesanan Baru</span>
              <Package className="w-5 h-5 text-teal-600" />
            </div>
            <div className="text-xl font-bold text-slate-900">{summary?.orders_count_today ?? 0}</div>
            <p className="text-xs text-slate-500 mt-1">Pesanan diterima hari ini</p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Sedang Diproses</span>
              <Activity className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-xl font-bold text-slate-900">{summary?.active_orders_count ?? 0}</div>
            <p className="text-xs text-slate-500 mt-1">Cuci, kering, setrika, packing</p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Siap Diambil/Diantar</span>
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <div className="text-xl font-bold text-emerald-700">{summary?.ready_orders_count ?? 0}</div>
            <p className="text-xs text-slate-500 mt-1">Menunggu serah terima pelanggan</p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs">
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider">Pesanan Terlambat</span>
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <div className="text-xl font-bold text-amber-700">{summary?.overdue_orders_count ?? 0}</div>
            <p className="text-xs text-slate-500 mt-1">Melebihi estimasi selesai</p>
          </div>
        </div>
      </div>
    </div>
  );
};


const AppContent: React.FC = () => {
  const { user, isLoading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  // Check if unauthenticated public customer tracking is requested
  const path = window.location.pathname;
  if (path.startsWith('/track/')) {
    const token = path.replace(/^\/track\//, '').split('/')[0];
    return <PublicTrackingPage token={token} />;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <Loader2 className="w-10 h-10 animate-spin text-teal-700 mb-4" />
        <p className="text-sm font-semibold text-slate-700">Memverifikasi sesi...</p>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <AppShell activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'dashboard' && <DashboardView />}
      {activeTab === 'orders' && <OrdersPage />}
      {activeTab === 'services' && <ServicesPage />}
      {activeTab === 'customers' && <CustomersPage />}
      {activeTab === 'users' && <UsersPage />}
      {activeTab === 'settings' && <SettingsPage />}
      {activeTab === 'delivery' && <DeliveryPage />}
      {activeTab === 'finance' && <ExpensesPage />}
      {activeTab === 'reports' && <ReportsPage />}
    </AppShell>
  );
};

export function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
