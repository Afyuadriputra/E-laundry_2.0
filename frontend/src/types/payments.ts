export type PaymentMethod = 'CASH' | 'BANK_TRANSFER' | 'QRIS_MANUAL';
export type PaymentStatus = 'UNPAID' | 'PARTIALLY_PAID' | 'PAID';

export interface Payment {
  id: string;
  order_id: string;
  amount: number;
  method: PaymentMethod;
  verification_status: string;
  payment_time: string;
  verified_by: string;
  verified_by_name: string | null;
  verified_at: string;
  reference_note: string | null;
  created_at: string;
  is_voided: boolean;
  void_reason: string | null;
  voided_at: string | null;
  voided_by_name: string | null;
}

export interface OrderPaymentSummary {
  order_id: string;
  order_number: string;
  total_amount: number;
  total_paid: number;
  remaining_amount: number;
  payment_status: PaymentStatus;
  payments: Payment[];
}

export interface RecordPaymentPayload {
  amount: number;
  method: PaymentMethod;
  reference_note?: string;
}

export interface VoidPaymentPayload {
  reason: string;
}

