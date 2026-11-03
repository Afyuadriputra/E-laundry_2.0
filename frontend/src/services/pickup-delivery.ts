import { apiClient, type ApiResponse } from '../lib/api-client';
import type {
  DeliveryTask,
  DeliveryTaskCreate,
  DeliveryTaskStatusUpdate,
  PickupConfirmPayload,
  PickupConvertToOrderPayload,
  PickupRejectPayload,
  PickupRequest,
} from '../types/pickup-delivery';

export const pickupDeliveryApi = {
  // Pickup Requests
  listPickupRequests: async (status?: string): Promise<PickupRequest[]> => {
    const qs = status ? `?status=${encodeURIComponent(status)}` : '';
    const res = await apiClient<ApiResponse<PickupRequest[]>>(`/pickup-delivery/requests${qs}`);
    return res.data;
  },

  getPickupRequest: async (id: string): Promise<PickupRequest> => {
    const res = await apiClient<ApiResponse<PickupRequest>>(`/pickup-delivery/requests/${id}`);
    return res.data;
  },

  confirmPickupRequest: async (
    id: string,
    payload: PickupConfirmPayload,
  ): Promise<PickupRequest> => {
    const res = await apiClient<ApiResponse<PickupRequest>>(
      `/pickup-delivery/requests/${id}/confirm`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
    return res.data;
  },

  rejectPickupRequest: async (
    id: string,
    payload: PickupRejectPayload,
  ): Promise<PickupRequest> => {
    const res = await apiClient<ApiResponse<PickupRequest>>(
      `/pickup-delivery/requests/${id}/reject`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
    return res.data;
  },

  convertToOrder: async (
    id: string,
    payload: PickupConvertToOrderPayload,
  ): Promise<{ order_id: string; order_number: string; total_amount: number }> => {
    const res = await apiClient<ApiResponse<{ order_id: string; order_number: string; total_amount: number }>>(
      `/pickup-delivery/requests/${id}/convert-order`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
    return res.data;
  },

  // Delivery Tasks
  listDeliveryTasks: async (params?: {
    status?: string;
    courier_user_id?: string;
    task_type?: string;
  }): Promise<DeliveryTask[]> => {
    const searchParams = new URLSearchParams();
    if (params?.status) searchParams.set('status', params.status);
    if (params?.courier_user_id) searchParams.set('courier_user_id', params.courier_user_id);
    if (params?.task_type) searchParams.set('task_type', params.task_type);

    const qs = searchParams.toString();
    const url = `/pickup-delivery/tasks${qs ? `?${qs}` : ''}`;
    const res = await apiClient<ApiResponse<DeliveryTask[]>>(url);
    return res.data;
  },

  listMyTasks: async (): Promise<DeliveryTask[]> => {
    const res = await apiClient<ApiResponse<DeliveryTask[]>>('/pickup-delivery/tasks/my-tasks');
    return res.data;
  },

  getDeliveryTask: async (id: string): Promise<DeliveryTask> => {
    const res = await apiClient<ApiResponse<DeliveryTask>>(`/pickup-delivery/tasks/${id}`);
    return res.data;
  },

  createDeliveryTask: async (payload: DeliveryTaskCreate): Promise<DeliveryTask> => {
    const res = await apiClient<ApiResponse<DeliveryTask>>('/pickup-delivery/tasks', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  updateTaskStatus: async (
    id: string,
    payload: DeliveryTaskStatusUpdate,
  ): Promise<DeliveryTask> => {
    const res = await apiClient<ApiResponse<DeliveryTask>>(
      `/pickup-delivery/tasks/${id}/status`,
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
    return res.data;
  },
};

