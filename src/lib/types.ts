// src/lib/types.ts
// TypeScript type definitions for the application

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO string format (snake_case from API)
  due_date?: string | null; // ISO string format or null (snake_case from API)
  updated_at: string; // ISO string format (snake_case from API)
  user_id: string; // snake_case from API
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  name: string;
  email: string;
  password: string;
}