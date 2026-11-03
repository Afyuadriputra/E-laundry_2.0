import { apiClient, type ApiResponse } from '../lib/api-client';
import type {
  CancelTrackingOrderRequest,
  PublicCancellationResponse,
  PublicTrackingRead,
} from '../types/tracking';

export const trackingApi = {
  getTrackingData: async (token: string): Promise<PublicTrackingRead> => {
    const res = await apiClient<ApiResponse<PublicTrackingRead>>(`/tracking/${token}`);
    return res.data;
  },

  cancelOrder: async (
    token: string,
    payload?: CancelTrackingOrderRequest
  ): Promise<PublicCancellationResponse> => {
    const res = await apiClient<ApiResponse<PublicCancellationResponse>>(
      `/tracking/${token}/cancel`,
      {
        method: 'POST',
        body: JSON.stringify(payload || {}),
      }
    );
    return res.data;
  },
};

