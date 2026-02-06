// Real auth client that connects to the backend API
// This connects to the JWT-protected backend API

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

interface AuthClient {
  getSession: () => Promise<{ session: AuthSession | null } | null>;
  signIn: {
    email: (credentials: { email: string; password: string; redirectTo?: string }) => Promise<any>;
  };
  signUp: {
    email: (userData: { name: string; email: string; password: string; redirectTo?: string }) => Promise<any>;
  };
  signOut: () => Promise<void>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

// Helper function to construct the API URL
// For Vercel deployment, always use relative paths to leverage Next.js rewrites
function constructApiUrl(path: string): string {
  // Always use relative paths to leverage Next.js rewrites in Vercel
  return path;
}

export const authClient: AuthClient = {
  getSession: async () => {
    // Retrieve session from localStorage for persistence
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token');
      const storedUser = localStorage.getItem('auth_user');

      if (storedToken && storedUser) {
        const user = JSON.parse(storedUser);
        // For now, we'll assume the token is valid and create a mock session
        // In a real implementation, you would validate the token with the backend
        return {
          session: {
            user,
            token: storedToken,
            expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
          }
        };
      }
    }
    return null;
  },

  signIn: {
    email: async ({ email, password, redirectTo }) => {
      try {
        // Use FormData for OAuth2PasswordRequestForm compatibility
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const url = constructApiUrl('/auth/token');
        console.log(`Making request to: ${url}`);
        console.log('FormData contents:', Array.from(formData.entries()));

        const response = await fetch(url, {
          method: 'POST',
          body: formData,
          // Don't set Content-Type header when using FormData - browser sets it with the correct boundary
          mode: 'cors',
          credentials: 'include',
        });

        console.log('Response received:', response.status);

        console.log(`Response status: ${response.status}`);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('Auth error response:', errorData);
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Auth response data:', data);

        const token = data.access_token;

        // Decode the JWT to get user info
        const tokenParts = token.split('.');
        if (tokenParts.length === 3) {
          const payload = JSON.parse(atob(tokenParts[1]));
          const user = {
            id: payload.sub,
            email: payload.email || email,
            name: payload.name || email.split('@')[0],
          };

          // Store the token and user in localStorage
          if (typeof window !== 'undefined') {
            localStorage.setItem('auth_token', token);
            localStorage.setItem('auth_user', JSON.stringify(user));
            console.log('Auth tokens stored in localStorage');
          }

          // Return session data
          return {
            session: {
              user,
              token,
              expiresAt: new Date(payload.exp * 1000) // Convert Unix timestamp to Date
            }
          };
        } else {
          throw new Error('Invalid token format');
        }
      } catch (error) {
        console.error('Sign in error:', error);
        if (error instanceof TypeError && error.message.includes('fetch')) {
          throw new Error('Network error: Unable to connect to authentication server. Please check that the backend is running on the correct port.');
        }
        throw error;
      }
    }
  },

  signUp: {
    email: async ({ name, email, password, redirectTo }) => {
      try {
        const url = constructApiUrl('/auth/register');
        console.log(`Making request to: ${url}`);

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, email, password }),
          mode: 'cors',
          credentials: 'include',
        });

        console.log(`Response status: ${response.status}`);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('Registration error response:', errorData);
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        // After registration, automatically sign in the user
        return await authClient.signIn.email({ email, password, redirectTo });
      } catch (error) {
        console.error('Sign up error:', error);
        if (error instanceof TypeError && error.message.includes('fetch')) {
          throw new Error('Network error: Unable to connect to authentication server. Please check that the backend is running on the correct port.');
        }
        throw error;
      }
    }
  },

  signOut: async () => {
    // Clear the stored token and user
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
    }
  }
};