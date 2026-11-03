export type PricingType = 'PER_KG' | 'PER_ITEM';
export type ServiceUnit = 'KG' | 'PCS';

export interface LaundryService {
  id: string;
  business_id: string;
  name: string;
  pricing_type: PricingType;
  unit: ServiceUnit;
  unit_price: number;
  estimated_hours?: number | null;
  requires_ironing: boolean;
  is_active: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface ServiceCreateInput {
  name: string;
  pricing_type: PricingType;
  unit: ServiceUnit;
  unit_price: number;
  estimated_hours?: number;
  requires_ironing: boolean;
}

export interface ServiceUpdateInput {
  name?: string;
  pricing_type?: PricingType;
  unit?: ServiceUnit;
  unit_price?: number;
  estimated_hours?: number;
  requires_ironing?: boolean;
  is_active?: boolean;
}

