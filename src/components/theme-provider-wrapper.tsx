'use client';

import { ThemeProvider } from '@/context/theme-context';
import { AuthProvider } from '@/context/auth-context';
import { ReactNode, useEffect } from 'react';

export default function ThemeProviderWrapper({ children }: { children: ReactNode }) {
  // Ensure the theme class is applied to the html element on initial load
  useEffect(() => {
    // Get saved theme from localStorage or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Apply the theme class to the html element
    document.documentElement.className = savedTheme;
  }, []);

  return (
    <ThemeProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  );
}