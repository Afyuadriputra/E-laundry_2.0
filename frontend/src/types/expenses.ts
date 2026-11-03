export type ExpenseCategory =
  | 'DETERGENT'
  | 'FRAGRANCE'
  | 'PACKAGING'
  | 'ELECTRICITY'
  | 'WATER'
  | 'TRANSPORT'
  | 'EQUIPMENT_MAINTENANCE'
  | 'OTHER';

export interface Expense {
  id: string;
  business_id: string;
  category: ExpenseCategory;
  amount: number;
  expense_date: string;
  description: string | null;
  created_by: string;
  created_by_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateExpensePayload {
  category: ExpenseCategory;
  amount: number;
  expense_date: string;
  description?: string;
}

