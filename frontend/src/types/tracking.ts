export interface ServiceItemSummary {
  service_name: string;
  quantity: string;
  unit: string;
  unit_price: number;
  line_total: number;
}

export interface FinancialSummary {
  total_amount: number;
  paid_amount: number;
  remaining_amount: number;
  payment_status: 'UNPAID' | 'PARTIALLY_PAID' | 'PAID';
}

export interface TimelineEvent {
  status: string;
  status_label: string;
  timestamp: string;
  note?: string | null;
}

export interface BusinessContact {
  name: string;
  phone: string;
  address: string;
  whatsapp_url: string;
}

export interface PublicTrackingRead {
  tracking_type: 'ORDER' | 'PICKUP_REQUEST';
  order_number: string | null;
  current_status: string;
  status_label: string;
  can_cancel: boolean;
  created_at: string;
  estimated_completion_at: string | null;
  customer_name_masked: string;
  customer_phone_masked: string;
  service_summary: ServiceItemSummary[];
  financial_summary: FinancialSummary;
  timeline: TimelineEvent[];
  business_contact: BusinessContact;
  intake_method: string | null;
  return_method: string | null;
}

export interface CancelTrackingOrderRequest {
  reason?: string;
}

export interface PublicCancellationResponse {
  success: boolean;
  order_number: string;
  new_status: string;
  message: string;
  cancelled_at: string;
}

