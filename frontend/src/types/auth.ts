export type UserRole = 'OWNER' | 'CASHIER' | 'STAFF' | 'COURIER';

export interface UserSummary {
  id: string;
  username: string;
  full_name: string;
  role: UserRole;
  business_id: string;
  phone_e164: string | null;
  is_active: boolean;
}

export interface LoginResponseData {
  user: UserSummary;
  csrf_token: string;
}

export interface BusinessProfile {
  id: string;
  name: string;
  phone_e164: string;
  address: string;
  logo_path: string | null;
  timezone: string;
  is_active: boolean;
}

