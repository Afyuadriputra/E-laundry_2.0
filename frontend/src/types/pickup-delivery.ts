export type PickupStatus =
  | 'REQUESTED'
  | 'CONFIRMED'
  | 'ASSIGNED'
  | 'PICKED_UP'
  | 'CONVERTED'
  | 'CANCELLED'
  | 'REJECTED';

export type DeliveryTaskStatus =
  | 'PENDING'
  | 'ASSIGNED'
  | 'EN_ROUTE'
  | 'ARRIVED'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED';

export type DeliveryTaskType = 'PICKUP' | 'DELIVERY';

export interface PickupRequest {
  id: string;
  business_id: string;
  customer_id?: string | null;
  request_number: string;
  requester_name: string;
  phone_e164: string;
  pickup_address: string;
  requested_date: string;
  requested_time_start: string;
  requested_time_end: string;
  confirmed_start_at?: string | null;
  confirmed_end_at?: string | null;
  status: PickupStatus;
  notes?: string | null;
  rejection_reason?: string | null;
  created_at: string;
  updated_at: string;
  tracking_token?: string | null;
  tracking_url?: string | null;
}

export interface DeliveryStatusHistory {
  id: string;
  from_status?: string | null;
  to_status: DeliveryTaskStatus;
  changed_by_name?: string | null;
  reason?: string | null;
  created_at: string;
}

export interface DeliveryTask {
  id: string;
  business_id: string;
  task_type: DeliveryTaskType;
  pickup_request_id?: string | null;
  order_id?: string | null;
  order_number?: string | null;
  courier_user_id?: string | null;
  courier_name?: string | null;
  scheduled_start_at?: string | null;
  scheduled_end_at?: string | null;
  status: DeliveryTaskStatus;
  recipient_name?: string | null;
  destination_address: string;
  destination_phone?: string | null;
  proof_photo_path?: string | null;
  completed_at?: string | null;
  failure_reason?: string | null;
  created_at: string;
  updated_at: string;
  history?: DeliveryStatusHistory[];
}

export interface PickupConfirmPayload {
  confirmed_start_at: string;
  confirmed_end_at: string;
  courier_user_id?: string | null;
  notes?: string | null;
}

export interface PickupRejectPayload {
  rejection_reason: string;
}

export interface PickupConvertToOrderPayload {
  service_id: string;
  quantity: number;
  extra_charge_amount?: number;
  delivery_fee_amount?: number;
  return_method?: 'SELF_PICKUP' | 'HOME_DELIVERY';
  customer_notes?: string;
  internal_notes?: string;
}

export interface DeliveryTaskCreate {
  task_type: DeliveryTaskType;
  pickup_request_id?: string;
  order_id?: string;
  courier_user_id?: string;
  scheduled_start_at?: string;
  scheduled_end_at?: string;
  recipient_name?: string;
  destination_address: string;
  destination_phone?: string;
}

export interface DeliveryTaskStatusUpdate {
  to_status: DeliveryTaskStatus;
  failure_reason?: string;
  proof_photo_path?: string;
  received_by_name?: string;
  notes?: string;
}

