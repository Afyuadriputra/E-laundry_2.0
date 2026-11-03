import React, { useEffect, useState } from 'react';
import {
  DollarSign,
  Plus,
  Trash2,
  Filter,
  AlertCircle,
  Tag,
  Loader2,
  X,
  CheckCircle2,
} from 'lucide-react';
import { expensesApi } from '../../services/expenses';
import { useAuth } from '../../context/use-auth';
import type { Expense, ExpenseCategory } from '../../types/expenses';

const CATEGORY_LABELS: Record<ExpenseCategory, string> = {
  DETERGENT: 'Deterjen',
  FRAGRANCE: 'Pewangi / Parfum',
  PACKAGING: 'Plastik & Kemasan',
  ELECTRICITY: 'Listrik & PLN',
  WATER: 'Air & PDAM',
  TRANSPORT: 'Bensin & Transportasi',
  EQUIPMENT_MAINTENANCE: 'Servis Mesin & Alat',
  OTHER: 'Lain-lain',
};

export const ExpensesPage: React.FC = () => {
  const { user } = useAuth();
  const isOwner = user?.role === 'OWNER';

  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);

  // Form State
  const [category, setCategory] = useState<ExpenseCategory>('DETERGENT');
  const [amount, setAmount] = useState<number>(50000);
  const [expenseDate, setExpenseDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [description, setDescription] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadExpenses = async () => {
    try {
      const data = await expensesApi.listExpenses({
        category: selectedCategory || undefined,
      });
      setExpenses(data);
    } catch (err) {
      console.error('Failed to load expenses', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;
    async function fetchData() {
      try {
        const data = await expensesApi.listExpenses({
          category: selectedCategory || undefined,
        });
        if (!ignore) {
          setExpenses(data);
        }
      } catch (err) {
        console.error('Failed to load expenses', err);
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
  }, [selectedCategory]);

  const handleCreateExpense = async (e: React.FormEvent) => {
    e.preventDefault();
    if (amount <= 0) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await expensesApi.createExpense({
        category,
        amount,
        expense_date: expenseDate,
        description: description || undefined,
      });
      setIsModalOpen(false);
      setDescription('');
      loadExpenses();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal menyimpan pengeluaran.';
      setErrorMessage(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteExpense = async (id: string) => {
    try {
      await expensesApi.deleteExpense(id);
      setDeleteConfirmId(null);
      loadExpenses();
    } catch (err) {
      console.error('Failed to delete expense', err);
    }
  };

  const totalExpenseSum = expenses.reduce((acc, curr) => acc + curr.amount, 0);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 mb-1.5">
            <DollarSign className="w-3.5 h-3.5" />
            <span>Manajemen Finansial</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Pengeluaran Operasional</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Pencatatan biaya deterjen, listrik, kemasan, dan pemeliharaan outlet.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-xs font-semibold text-white bg-teal-700 hover:bg-teal-800 rounded-xl shadow-sm min-h-[44px] transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Catat Pengeluaran</span>
        </button>
      </div>

      {/* Highlights & Filter Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs sm:col-span-1">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Pengeluaran</span>
          <div className="text-2xl font-bold text-slate-900 mt-1">
            Rp {totalExpenseSum.toLocaleString('id-ID')}
          </div>
          <p className="text-xs text-slate-500 mt-0.5">{expenses.length} transaksi tercatat</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs sm:col-span-2 flex flex-col justify-center">
          <label className="text-xs font-semibold text-slate-700 mb-1.5 flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Filter Berdasarkan Kategori</span>
          </label>
          <div className="flex flex-wrap gap-1.5">
            <button
              type="button"
              onClick={() => setSelectedCategory('')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                selectedCategory === ''
                  ? 'bg-teal-700 text-white font-semibold'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              Semua
            </button>
            {(Object.keys(CATEGORY_LABELS) as ExpenseCategory[]).map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  selectedCategory === cat
                    ? 'bg-teal-700 text-white font-semibold'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {CATEGORY_LABELS[cat]}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Expenses Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        {isLoading ? (
          <div className="py-16 flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="w-8 h-8 animate-spin text-teal-700 mb-2" />
            <p className="text-xs">Memuat daftar pengeluaran...</p>
          </div>
        ) : expenses.length === 0 ? (
          <div className="py-16 text-center text-slate-500">
            <Tag className="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <p className="text-sm font-semibold text-slate-700">Belum Ada Pengeluaran</p>
            <p className="text-xs text-slate-500 mt-1">Belum ada transaksi operasional yang dicatat.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-3.5">Tanggal</th>
                  <th className="p-3.5">Kategori</th>
                  <th className="p-3.5">Keterangan</th>
                  <th className="p-3.5">Dicatat Oleh</th>
                  <th className="p-3.5 text-right">Nominal (Rp)</th>
                  {isOwner && <th className="p-3.5 text-center">Aksi</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {expenses.map((exp) => (
                  <tr key={exp.id} className="hover:bg-slate-50/50">
                    <td className="p-3.5 font-medium text-slate-900 whitespace-nowrap">
                      {new Date(exp.expense_date).toLocaleDateString('id-ID')}
                    </td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700">
                        {CATEGORY_LABELS[exp.category] || exp.category}
                      </span>
                    </td>
                    <td className="p-3.5 text-slate-600 max-w-xs truncate">{exp.description || '-'}</td>
                    <td className="p-3.5 text-slate-500">{exp.created_by_name || '-'}</td>
                    <td className="p-3.5 text-right font-bold text-slate-900">
                      Rp {exp.amount.toLocaleString('id-ID')}
                    </td>
                    {isOwner && (
                      <td className="p-3.5 text-center">
                        <button
                          type="button"
                          onClick={() => setDeleteConfirmId(exp.id)}
                          className="p-1.5 rounded-lg text-rose-500 hover:bg-rose-50 hover:text-rose-700 min-h-[36px] min-w-[36px] inline-flex items-center justify-center transition-colors"
                          title="Hapus pengeluaran"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create Expense Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
              <h3 className="text-base font-bold text-slate-900">Catat Pengeluaran Operasional</h3>
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
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

            <form onSubmit={handleCreateExpense} noValidate className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Kategori Pengeluaran</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value as ExpenseCategory)}
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl bg-white"
                >
                  {(Object.keys(CATEGORY_LABELS) as ExpenseCategory[]).map((cat) => (
                    <option key={cat} value={cat}>
                      {CATEGORY_LABELS[cat]}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Nominal (Rp)</label>
                <input
                  type="number"
                  min={100}
                  step={1000}
                  value={amount}
                  onChange={(e) => setAmount(parseInt(e.target.value, 10) || 0)}
                  required
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Tanggal Transaksi</label>
                <input
                  type="date"
                  value={expenseDate}
                  onChange={(e) => setExpenseDate(e.target.value)}
                  required
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Deskripsi / Keterangan (Opsional)</label>
                <textarea
                  rows={2}
                  placeholder="Misal: Beli sabun cair 2 jerigen di Toko Sumber Wangi"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl"
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100 rounded-xl"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || amount <= 0}
                  className="px-5 py-2 text-xs font-semibold text-white bg-teal-700 hover:bg-teal-800 disabled:opacity-50 rounded-xl flex items-center gap-1.5 shadow-sm"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{isSubmitting ? 'Menyimpan...' : 'Simpan Pengeluaran'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirmId && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xl max-w-sm w-full p-6 text-center">
            <Trash2 className="w-10 h-10 text-rose-600 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-900">Hapus Catatan Pengeluaran?</h3>
            <p className="text-xs text-slate-500 mt-1 mb-4">
              Tindakan ini tidak dapat dibatalkan dan akan menghapus transaksi dari pembukuan outlet.
            </p>
            <div className="flex items-center justify-center gap-2">
              <button
                type="button"
                onClick={() => setDeleteConfirmId(null)}
                className="px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100 rounded-xl"
              >
                Batal
              </button>
              <button
                type="button"
                onClick={() => handleDeleteExpense(deleteConfirmId)}
                className="px-4 py-2 text-xs font-semibold text-white bg-rose-700 hover:bg-rose-800 rounded-xl shadow-sm"
              >
                Hapus
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
