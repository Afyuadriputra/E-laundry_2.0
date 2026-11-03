import { apiClient, type ApiResponse } from '../lib/api-client';
import type { Invoice } from '../types/invoices';

export const invoicesApi = {
  getInvoice: async (orderId: string): Promise<Invoice> => {
    const res = await apiClient<ApiResponse<Invoice>>(`/invoices/${orderId}`);
    return res.data;
  },

  getThermalUrl: (orderId: string): string => `/api/v1/invoices/${orderId}/thermal`,
  getHtmlUrl: (orderId: string): string => `/api/v1/invoices/${orderId}/html`,
};

