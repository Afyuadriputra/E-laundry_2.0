import { apiClient, type ApiResponse } from '../lib/api-client';
import type {
  DashboardSummary,
  FinancialReportSummary,
  OrdersReportSummary,
  OutstandingBalanceItem,
  OverdueOrder,
} from '../types/reports';

export const reportsApi = {
  getDashboardSummary: async (params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<DashboardSummary> => {
    const searchParams = new URLSearchParams();
    if (params?.start_date) searchParams.set('start_date', params.start_date);
    if (params?.end_date) searchParams.set('end_date', params.end_date);
    const qs = searchParams.toString();
    const res = await apiClient<ApiResponse<DashboardSummary>>(
      `/reports/dashboard${qs ? `?${qs}` : ''}`
    );
    return res.data;
  },

  getOverdueOrders: async (): Promise<OverdueOrder[]> => {
    const res = await apiClient<ApiResponse<OverdueOrder[]>>('/reports/overdue');
    return res.data;
  },

  getOrdersReport: async (params?: {
    start_date?: string;
    end_date?: string;
    operational_status?: string;
    payment_status?: string;
  }): Promise<OrdersReportSummary> => {
    const searchParams = new URLSearchParams();
    if (params?.start_date) searchParams.set('start_date', params.start_date);
    if (params?.end_date) searchParams.set('end_date', params.end_date);
    if (params?.operational_status)
      searchParams.set('operational_status', params.operational_status);
    if (params?.payment_status)
      searchParams.set('payment_status', params.payment_status);

    const qs = searchParams.toString();
    const res = await apiClient<ApiResponse<OrdersReportSummary>>(
      `/reports/orders${qs ? `?${qs}` : ''}`
    );
    return res.data;
  },

  getFinancialReport: async (params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<FinancialReportSummary> => {
    const searchParams = new URLSearchParams();
    if (params?.start_date) searchParams.set('start_date', params.start_date);
    if (params?.end_date) searchParams.set('end_date', params.end_date);
    const qs = searchParams.toString();
    const res = await apiClient<ApiResponse<FinancialReportSummary>>(
      `/reports/finances${qs ? `?${qs}` : ''}`
    );
    return res.data;
  },

  getOutstandingReport: async (): Promise<OutstandingBalanceItem[]> => {
    const res = await apiClient<ApiResponse<OutstandingBalanceItem[]>>(
      '/reports/outstanding'
    );
    return res.data;
  },

  downloadCsv: async (endpoint: string, filename: string): Promise<void> => {
    const res = await fetch(`/api/v1${endpoint}`, {
      credentials: 'include',
    });
    if (!res.ok) {
      throw new Error(`Gagal mengunduh CSV: status ${res.status}`);
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },
};

