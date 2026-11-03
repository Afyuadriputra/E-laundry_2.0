export interface Customer {
  id: string;
  business_id: string;
  full_name: string;
  phone_e164: string;
  address?: string | null;
  notes?: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  total_orders?: number;
}

export interface CustomerCreateInput {
  full_name: string;
  phone_e164: string;
  address?: string;
  notes?: string;
}

export interface CustomerUpdateInput {
  full_name?: string;
  phone_e164?: string;
  address?: string;
  notes?: string;
  is_active?: boolean;
}
