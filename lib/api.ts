// src/lib/api.ts
// Centralized API client that automatically attaches Authorization header to requests
// and handles 401 responses by redirecting to login

import { redirect } from 'next/navigation';

class ApiClient {
  private baseUrl: string;

  constructor() {
    // Use relative path if NEXT_PUBLIC_API_BASE_URL is not set or is empty
    const envBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    this.baseUrl = (envBaseUrl && envBaseUrl.trim() !== '')
      ? envBaseUrl
      : ''; // Empty string means relative path
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    // For Vercel deployment, use relative paths to leverage Next.js rewrites
    // This ensures requests are properly proxied to the backend
    const url = endpoint;

    // Determine if this is an auth endpoint (should not include auth token)
    const isAuthEndpoint = endpoint.includes('/auth/');

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    } as Record<string, string>;

    // Only add Authorization header if not an auth endpoint
    if (!isAuthEndpoint) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        // Add mode: 'cors' to explicitly enable CORS
        mode: 'cors',
        // Add credentials to include cookies if needed
        credentials: 'include',
      });

      // Handle 401 Unauthorized responses (only for non-auth endpoints)
      if (response.status === 401 && !isAuthEndpoint) {
        // Clear any stored tokens
        this.clearAuthToken();
        // Redirect to login page
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return;
      }

      if (!response.ok) {
        // Try to get error details from response
        let errorMessage = `API request failed: ${response.status} ${response.statusText}`;
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            errorMessage = `${errorMessage} - ${errorData.detail}`;
          }
        } catch (e) {
          // If response is not JSON, use the status text
        }
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Could not connect to the server. Please make sure the backend is running and accessible.');
      }
      throw error;
    }
  }

  private getAuthToken(): string | null {
    // In a real implementation, you would retrieve the token from cookies or storage
    // This is a placeholder implementation
    if (typeof window !== 'undefined') {
      // Client-side code
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private clearAuthToken(): void {
    // In a real implementation, you would clear the token from cookies or storage
    if (typeof window !== 'undefined') {
      // Client-side code
      localStorage.removeItem('auth_token');
    }
  }

  get<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'GET' });
  }

  post<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  }

  patch<T>(endpoint: string, data: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  }

  delete<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();