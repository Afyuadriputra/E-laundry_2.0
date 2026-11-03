import type { Customer } from './customers';

export type OperationalStatus =
  | 'RECEIVED'
  | 'QUEUED'
  | 'WASHING'
  | 'DRYING'
  | 'IRONING'
  | 'QC_PACKING'
  | 'READY'
  | 'COMPLETED'
  | 'CANCELLED';

export type IntakeMethod = 'DROP_OFF' | 'COURIER_PICKUP';
export type ReturnMethod = 'SELF_PICKUP' | 'HOME_DELIVERY';

export interface OrderItem {
  id: string;
  service_id: string;
  service_name_snapshot: string;
  pricing_type_snapshot: string;
  unit_snapshot: string;
  quantity: string | number;
  unit_price_snapshot: number;
  line_total_amount: number;
  requires_ironing_snapshot: boolean;
  created_at: string;
}

export interface OrderStatusHistoryItem {
  id: string;
  from_status?: string | null;
  to_status: string;
  changed_by: string;
  reason?: string | null;
  created_at: string;
}

export interface OrderHandoff {
  id: string;
  handoff_method: string;
  received_by_name?: string | null;
  confirmed_by_user_id: string;
  confirmed_at: string;
  notes?: string | null;
}

export interface OrderListItem {
  id: string;
  business_id: string;
  order_number: string;
  customer_id: string;
  customer_name: string;
  customer_phone: string;
  operational_status: OperationalStatus;
  intake_method: IntakeMethod;
  return_method: ReturnMethod;
  total_amount: number;
  subtotal_amount: number;
  extra_charge_amount: number;
  delivery_fee_amount: number;
  estimated_completion_at: string;
  version: number;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
  cancelled_at?: string | null;
}

export interface OrderDetail extends OrderListItem {
  customer: Customer;
  items: OrderItem[];
  status_history: OrderStatusHistoryItem[];
  handoff?: OrderHandoff | null;
  customer_notes?: string | null;
  internal_notes?: string | null;
  cancellation_reason?: string | null;
}

export interface OrderItemInput {
  service_id: string;
  quantity: string;
}

export interface OrderCreateInput {
  customer_id?: string;
  new_customer_name?: string;
  new_customer_phone?: string;
  new_customer_address?: string;
  items: OrderItemInput[];
  intake_method: IntakeMethod;
  return_method: ReturnMethod;
  extra_charge_amount: number;
  delivery_fee_amount: number;
  estimated_completion_at?: string;
  customer_notes?: string;
  internal_notes?: string;
}

export interface OrderTransitionInput {
  to_status: OperationalStatus;
  reason?: string;
  cancellation_reason?: string;
  expected_version: number;
}
