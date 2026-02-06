'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient } from '@/lib/auth';

// Define types based on the new auth client
interface AuthUser {
  id: string;
  email: string;
  name?: string;
}

interface AuthSession {
  user: AuthUser;
  token: string;
  expiresAt: Date;
}

interface AuthContextType {
  user: AuthUser | null;
  session: AuthSession | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session when component mounts
    // Only run on client side to prevent SSR issues
    if (typeof window !== 'undefined') {
      const checkSession = async () => {
        try {
          const currentSession = await authClient.getSession();
          setSession(currentSession?.session || null);
        } catch (error) {
          console.error('Error checking session:', error);
          setSession(null);
        } finally {
          setLoading(false);
        }
      };

      checkSession();
    } else {
      // On server side, set loading to false and session to null
      setSession(null);
      setLoading(false);
    }
  }, []);

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      const result = await authClient.signIn.email({
        email,
        password,
        redirectTo: '/dashboard',
      });

      // Update session state with the login result
      if (result?.session) {
        setSession(result.session);
      }
    } catch (error: any) {
      console.error('Sign in error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    setLoading(true);
    try {
      await authClient.signOut();
      setSession(null);
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      setLoading(false);
    }
  };

  const signUp = async (name: string, email: string, password: string) => {
    setLoading(true);
    try {
      const result = await authClient.signUp.email({
        name,
        email,
        password,
        redirectTo: '/dashboard',
      });

      // Update session state with the new user data
      if (result?.session) {
        setSession(result.session);
      }

      return result;
    } catch (error: any) {
      console.error('Sign up error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user: session?.user || null,
    session,
    loading,
    signIn,
    signOut,
    signUp,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}