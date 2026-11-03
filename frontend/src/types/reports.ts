export interface DashboardSummary {
  orders_count_today: number;
  active_orders_count: number;
  ready_orders_count: number;
  completed_orders_today: number;
  overdue_orders_count: number;

  order_value_period?: number | null;
  cash_received_period?: number | null;
  expenses_period?: number | null;
  simple_cash_difference?: number | null;
  outstanding_receivables?: number | null;

  start_date: string;
  end_date: string;
}

export interface OverdueOrder {
  order_id: string;
  order_number: string;
  customer_name: string;
  customer_phone: string;
  operational_status: string;
  estimated_completion_at: string;
  hours_overdue: number;
  total_amount: number;
  remaining_amount: number;
}

export interface OrdersReportItem {
  order_id: string;
  order_number: string;
  created_at: string;
  customer_name: string;
  customer_phone: string;
  operational_status: string;
  payment_status: string;
  total_amount: number;
  paid_amount: number;
  remaining_amount: number;
  items_summary: string;
}

export interface OrdersReportSummary {
  total_orders: number;
  total_amount: number;
  total_paid: number;
  total_outstanding: number;
  items: OrdersReportItem[];
}

export interface FinancialReportSummary {
  start_date: string;
  end_date: string;
  total_cash_received: number;
  cash_by_method: Record<string, number>;
  total_expenses: number;
  expenses_by_category: Record<string, number>;
  simple_cash_difference: number;
  outstanding_receivables: number;
}

export interface OutstandingBalanceItem {
  order_id: string;
  order_number: string;
  created_at: string;
  customer_name: string;
  customer_phone: string;
  total_amount: number;
  paid_amount: number;
  remaining_amount: number;
  payment_status: string;
  operational_status: string;
}

