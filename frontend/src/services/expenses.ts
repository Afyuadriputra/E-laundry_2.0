import { apiClient, type ApiResponse } from '../lib/api-client';
import type { CreateExpensePayload, Expense } from '../types/expenses';

export const expensesApi = {
  listExpenses: async (params?: { category?: string; start_date?: string; end_date?: string }): Promise<Expense[]> => {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.set('category', params.category);
    if (params?.start_date) searchParams.set('start_date', params.start_date);
    if (params?.end_date) searchParams.set('end_date', params.end_date);

    const qs = searchParams.toString();
    const url = `/expenses${qs ? `?${qs}` : ''}`;
    const res = await apiClient<ApiResponse<Expense[]>>(url);
    return res.data;
  },

  createExpense: async (payload: CreateExpensePayload): Promise<Expense> => {
    const res = await apiClient<ApiResponse<Expense>>('/expenses', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  deleteExpense: async (id: string): Promise<void> => {
    await apiClient<ApiResponse<{ message: string }>>(`/expenses/${id}`, {
      method: 'DELETE',
    });
  },
};

