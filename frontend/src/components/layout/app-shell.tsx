import React, { useState } from 'react';
import { useAuth } from '../../context/use-auth';
import {
  LogOut,
  Menu,
  X,
  ShoppingBag,
  Users,
  Truck,
  CreditCard,
  UserCheck,
  Settings,
  ShieldCheck,
  FileText,
} from 'lucide-react';

interface AppShellProps {
  children: React.ReactNode;
  activeTab?: string;
  onTabChange?: (tab: string) => void;
}

export const AppShell: React.FC<AppShellProps> = ({
  children,
  activeTab = 'dashboard',
  onTabChange,
}) => {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  if (!user) return null;

  const role = user.role;

  // Role-based navigation items matching BSD.md section 30
  const navItems = [
    {
      id: 'dashboard',
      label: 'Ringkasan',
      icon: ShoppingBag,
      visible: true,
    },
    {
      id: 'orders',
      label: 'Pesanan',
      icon: ShoppingBag,
      visible: ['OWNER', 'CASHIER', 'STAFF'].includes(role),
    },
    {
      id: 'services',
      label: 'Layanan',
      icon: ShieldCheck,
      visible: ['OWNER', 'CASHIER', 'STAFF'].includes(role),
    },
    {
      id: 'customers',
      label: 'Pelanggan',
      icon: Users,
      visible: ['OWNER', 'CASHIER'].includes(role),
    },
    {
      id: 'delivery',
      label: 'Antar-Jemput',
      icon: Truck,
      visible: ['OWNER', 'CASHIER', 'COURIER'].includes(role),
    },
    {
      id: 'finance',
      label: 'Keuangan',
      icon: CreditCard,
      visible: ['OWNER', 'CASHIER'].includes(role),
    },
    {
      id: 'reports',
      label: 'Laporan',
      icon: FileText,
      visible: ['OWNER', 'CASHIER'].includes(role),
    },
    {
      id: 'users',
      label: 'Pegawai',
      icon: UserCheck,
      visible: role === 'OWNER',
    },
    {
      id: 'settings',
      label: 'Pengaturan',
      icon: Settings,
      visible: role === 'OWNER',
    },
  ].filter((item) => item.visible);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
    } finally {
      setIsLoggingOut(false);
    }
  };

  const getRoleBadge = (r: string) => {
    switch (r) {
      case 'OWNER':
        return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800">Owner</span>;
      case 'CASHIER':
        return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">Kasir</span>;
      case 'STAFF':
        return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">Staf</span>;
      case 'COURIER':
        return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800">Kurir</span>;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row">
      {/* Mobile Top Navbar */}
      <header className="md:hidden bg-white border-b border-slate-200 px-4 py-3 flex items-center justify-between sticky top-0 z-40">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-teal-700 text-white flex items-center justify-center font-bold text-sm">
            EL
          </div>
          <div>
            <div className="text-sm font-bold text-slate-900 leading-tight">E-Laundry 2.0</div>
            <div className="text-xs text-slate-500">{user.full_name}</div>
          </div>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 rounded-xl text-slate-600 hover:bg-slate-100 min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </header>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-[61px] bg-slate-900/40 backdrop-blur-xs z-30">
          <div className="bg-white border-b border-slate-200 p-4 space-y-1">
            <div className="px-3 py-2 mb-2 flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <p className="text-sm font-semibold text-slate-900">{user.full_name}</p>
                <p className="text-xs text-slate-500">@{user.username}</p>
              </div>
              {getRoleBadge(user.role)}
            </div>

            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onTabChange?.(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium min-h-[44px] transition-colors ${
                    isActive
                      ? 'bg-teal-50 text-teal-800 font-semibold'
                      : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-teal-700' : 'text-slate-500'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}

            <div className="pt-3 mt-2 border-t border-slate-100">
              <button
                onClick={handleLogout}
                disabled={isLoggingOut}
                className="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium text-rose-700 hover:bg-rose-50 min-h-[44px] transition-colors"
              >
                <LogOut className="w-5 h-5" />
                <span>{isLoggingOut ? 'Keluar...' : 'Keluar Akun'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Desktop Sidebar Navigation */}
      <aside className="hidden md:flex flex-col w-64 bg-white border-r border-slate-200 min-h-screen p-5 shrink-0">
        <div className="flex items-center gap-3 px-2 mb-8">
          <div className="w-10 h-10 rounded-xl bg-teal-700 text-white flex items-center justify-center font-bold text-base shadow-sm">
            EL
          </div>
          <div>
            <div className="text-base font-bold text-slate-900 leading-tight">E-Laundry 2.0</div>
            <div className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
              <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
              <span>Sistem Operasional</span>
            </div>
          </div>
        </div>

        <nav className="flex-1 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange?.(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium min-h-[44px] transition-colors ${
                  isActive
                    ? 'bg-teal-50 text-teal-800 font-semibold shadow-xs'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-teal-700' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Card & Logout */}
        <div className="pt-4 border-t border-slate-200 mt-4 space-y-3">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-slate-900 truncate">{user.full_name}</span>
              {getRoleBadge(user.role)}
            </div>
            <p className="text-xs text-slate-500 truncate">@{user.username}</p>
          </div>

          <button
            onClick={handleLogout}
            disabled={isLoggingOut}
            className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl text-xs font-semibold text-rose-700 hover:bg-rose-50 border border-rose-200 min-h-[44px] transition-colors disabled:opacity-50"
          >
            <LogOut className="w-4 h-4" />
            <span>{isLoggingOut ? 'Keluar...' : 'Keluar Akun'}</span>
          </button>
        </div>
      </aside>

      {/* Main Content Viewport */}
      <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8 overflow-y-auto">
        <div className="max-w-6xl mx-auto">{children}</div>
      </main>
    </div>
  );
};
