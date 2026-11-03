import React, { useEffect, useState } from 'react';
import { apiClient, ApiError, type ApiResponse } from '../../lib/api-client';
import type { UserSummary } from '../../types/auth';
import {
  AlertCircle,
  CheckCircle2,
  Loader2,
  Plus,
  Shield,
  UserCheck,
  UserX,
} from 'lucide-react';

export const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<UserSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Modal / Form state
  const [showAddModal, setShowAddModal] = useState(false);
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'CASHIER' | 'STAFF' | 'COURIER'>('CASHIER');
  const [phone, setPhone] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchUsers = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await apiClient<ApiResponse<UserSummary[]>>('/users');
      setUsers(res.data);
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal memuat daftar pegawai.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const res = await apiClient<ApiResponse<UserSummary[]>>('/users');
        if (!ignore) {
          setUsers(res.data);
        }
      } catch (err) {
        if (!ignore) {
          if (err instanceof ApiError) {
            setErrorMsg(err.message);
          } else {
            setErrorMsg('Gagal memuat daftar pegawai.');
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

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!username.trim() || !fullName.trim() || !password) {
      setErrorMsg('Semua field wajib diisi.');
      return;
    }

    setIsSubmitting(true);
    try {
      await apiClient<ApiResponse<UserSummary>>('/users', {
        method: 'POST',
        body: JSON.stringify({
          username: username.trim(),
          full_name: fullName.trim(),
          password,
          role,
          phone_e164: phone.trim() || null,
        }),
      });
      setSuccessMsg(`Akun untuk "${fullName}" berhasil dibuat.`);
      setShowAddModal(false);
      setUsername('');
      setFullName('');
      setPassword('');
      setPhone('');
      await fetchUsers();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal menambahkan pegawai.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeactivate = async (user: UserSummary) => {
    if (!window.confirm(`Yakin ingin menonaktifkan akun @${user.username}? Sesi login aktif akan segera dicabut.`)) {
      return;
    }
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      await apiClient<ApiResponse<UserSummary>>(`/users/${user.id}/deactivate`, {
        method: 'POST',
      });
      setSuccessMsg(`Akun @${user.username} berhasil dinonaktifkan.`);
      await fetchUsers();
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Gagal menonaktifkan pengguna.');
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Manajemen Pegawai</h1>
          <p className="text-sm text-slate-500 mt-1">
            Kelola hak akses dan akun operasional kasir, staf cuci, dan kurir
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white font-medium text-sm shadow-sm min-h-[44px] transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Tambah Pegawai</span>
        </button>
      </div>

      {/* Notifications */}
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

      {/* Content Table / Cards */}
      {isLoading ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <Loader2 className="w-8 h-8 animate-spin text-teal-700 mx-auto mb-3" />
          <p className="text-sm text-slate-500 font-medium">Memuat data pegawai...</p>
        </div>
      ) : users.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <Shield className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-slate-800">Belum ada akun pegawai</h3>
          <p className="text-sm text-slate-500 mt-1 mb-4">Tambahkan kasir, kurir, atau staf cuci baru.</p>
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-700 text-white text-sm font-medium"
          >
            <Plus className="w-4 h-4" />
            <span>Tambah Sekarang</span>
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-5 py-3.5">Nama & Username</th>
                  <th className="px-5 py-3.5">Peran / Role</th>
                  <th className="px-5 py-3.5">No. Telepon</th>
                  <th className="px-5 py-3.5">Status</th>
                  <th className="px-5 py-3.5 text-right">Tindakan</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="px-5 py-4">
                      <div className="font-semibold text-slate-900">{u.full_name}</div>
                      <div className="text-xs text-slate-500">@{u.username}</div>
                    </td>
                    <td className="px-5 py-4">
                      <span className="inline-block px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-800">
                        {u.role}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-slate-600">{u.phone_e164 || '-'}</td>
                    <td className="px-5 py-4">
                      {u.is_active ? (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                          <UserCheck className="w-3.5 h-3.5" />
                          <span>Aktif</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200">
                          <UserX className="w-3.5 h-3.5" />
                          <span>Nonaktif</span>
                        </span>
                      )}
                    </td>
                    <td className="px-5 py-4 text-right">
                      {u.role !== 'OWNER' && u.is_active && (
                        <button
                          onClick={() => handleDeactivate(u)}
                          className="px-3 py-1.5 rounded-lg text-xs font-medium text-rose-700 hover:bg-rose-50 border border-rose-200 min-h-[36px] transition-colors"
                        >
                          Nonaktifkan
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Add User Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-200 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-1">Tambah Pegawai Baru</h2>
            <p className="text-xs text-slate-500 mb-6">
              Buat akun dengan hak akses sesuai tugas operasional.
            </p>

            <form onSubmit={handleCreateUser} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                  Nama Lengkap
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Contoh: Siti Rahmawati"
                  required
                  className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Contoh: kasir_siti"
                  required
                  className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                  Password Awal
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Minimal 8 karakter"
                  required
                  className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                  Peran / Role
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value as 'CASHIER' | 'STAFF' | 'COURIER')}
                  className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
                >
                  <option value="CASHIER">Kasir (Kelola pesanan, pembayaran, pelanggan)</option>
                  <option value="STAFF">Staf Cuci (Pembaruan status operasional cuci)</option>
                  <option value="COURIER">Kurir (Tugas penjemputan & pengantaran)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-slate-700 mb-1.5">
                  No. Telepon / WhatsApp (Opsional)
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+628123456789"
                  className="w-full min-h-[44px] px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-teal-700 focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2.5 rounded-xl text-slate-600 hover:bg-slate-100 text-sm font-medium min-h-[44px]"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-5 py-2.5 rounded-xl bg-teal-700 hover:bg-teal-800 text-white text-sm font-medium min-h-[44px] flex items-center gap-2 disabled:opacity-50"
                >
                  {isSubmitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  <span>Simpan Akun</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
