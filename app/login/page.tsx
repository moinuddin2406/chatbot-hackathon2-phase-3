'use client';

import React, { useState } from 'react';
import AuthForm from '@/components/auth/auth-form';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function LoginPage() {
  const { signIn } = useAuth();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (formData: Record<string, string>) => {
    setIsLoading(true);
    setError(null);

    try {
      await signIn(formData.email, formData.password);
      router.push('/dashboard');
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const fields = [
    { name: 'email', label: 'Email address', type: 'email', required: true },
    { name: 'password', label: 'Password', type: 'password', required: true },
  ];

  return (
    <div className="min-h-screen bg-[#0b0b12] flex flex-col">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 border-b border-transparent border-b-[linear-gradient(90deg,_#ff2bd6,_#9c27b0,_#38bdf8)]">
        <Link href="/">
          <div className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
            Todo App
          </div>
        </Link>
        <div>
          <Link href="/signup">
            <span className="text-[#00f5ff] hover:text-[#38bdf8] font-medium cursor-pointer transition-colors neon-glow">Sign Up</span>
          </Link>
        </div>
      </nav>

      <div className="flex flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8 animate-fade-in">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#ff2bd6] backdrop-blur-md rounded-2xl p-8 shadow-[0_0_15px_#ff2bd6]">
            <AuthForm
              title="Sign in to your account"
              fields={fields}
              submitButtonText="Sign in"
              isLoading={isLoading}
              errorMessage={error}
              onSubmit={handleLogin}
              toggleText="Don't have an account?"
              onToggleForm={() => router.push('/signup')}
            />
          </div>
        </div>
      </div>
    </div>
  );
}