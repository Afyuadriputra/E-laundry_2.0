import { createContext } from 'react';
import type { UserSummary } from '../types/auth';

export interface AuthContextType {
  user: UserSummary | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);
