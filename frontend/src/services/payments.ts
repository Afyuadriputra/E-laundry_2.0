import { apiClient, type ApiResponse } from '../lib/api-client';
import type {
  OrderPaymentSummary,
  Payment,
  RecordPaymentPayload,
  VoidPaymentPayload,
} from '../types/payments';

export const paymentsApi = {
  getOrderPaymentSummary: async (orderId: string): Promise<OrderPaymentSummary> => {
    const res = await apiClient<ApiResponse<OrderPaymentSummary>>(`/orders/${orderId}/payments`);
    return res.data;
  },

  recordPayment: async (
    orderId: string,
    payload: RecordPaymentPayload,
    idempotencyKey?: string,
  ): Promise<Payment> => {
    const headers: Record<string, string> = {};
    if (idempotencyKey) {
      headers['Idempotency-Key'] = idempotencyKey;
    }
    const res = await apiClient<ApiResponse<Payment>>(`/orders/${orderId}/payments`, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  voidPayment: async (paymentId: string, payload: VoidPaymentPayload): Promise<Payment> => {
    const res = await apiClient<ApiResponse<Payment>>(`/payments/${paymentId}/void`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },
};

