import React, { useCallback, useEffect, useState } from 'react';
import { apiClient, type ApiResponse } from '../lib/api-client';
import type { LoginResponseData, UserSummary } from '../types/auth';
import { AuthContext } from './auth-context-def';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserSummary | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = useCallback(async () => {
    try {
      const res = await apiClient<ApiResponse<UserSummary>>('/auth/me');
      setUser(res.data);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    async function initAuth() {
      try {
        const res = await apiClient<ApiResponse<UserSummary>>('/auth/me');
        if (!ignore) {
          setUser(res.data);
        }
      } catch {
        if (!ignore) {
          setUser(null);
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }
    initAuth();
    return () => {
      ignore = true;
    };
  }, []);

  const login = async (username: string, password: string) => {
    const res = await apiClient<ApiResponse<LoginResponseData>>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    setUser(res.data.user);
  };

  const logout = async () => {
    try {
      await apiClient<ApiResponse<{ message: string }>>('/auth/logout', {
        method: 'POST',
      });
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};
