export interface InvoiceItem {
  service_name: string;
  quantity: string;
  unit: string;
  unit_price: number;
  line_total: number;
}

export interface InvoicePayment {
  payment_time: string;
  method: string;
  amount: number;
}

export interface Invoice {
  order_id: string;
  order_number: string;
  created_at: string;
  estimated_completion_at: string;
  operational_status: string;

  business_name: string;
  business_phone: string;
  business_address: string;

  customer_name: string;
  customer_phone: string;
  intake_method: string;
  return_method: string;

  items: InvoiceItem[];
  subtotal_amount: number;
  extra_charge_amount: number;
  delivery_fee_amount: number;
  total_amount: number;
  total_paid: number;
  remaining_amount: number;
  payment_status: string;
  payments: InvoicePayment[];

  customer_notes?: string;
  tracking_url: string;
  whatsapp_share_url: string;
  whatsapp_share_text: string;
}

