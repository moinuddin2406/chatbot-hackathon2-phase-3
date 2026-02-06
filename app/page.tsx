'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [hasCheckedAuth, setHasCheckedAuth] = useState(false);

  useEffect(() => {
    // Check authentication status and redirect if needed
    if (!loading) {
      if (user) {
        // Authenticated user - redirect to dashboard
        router.push('/dashboard');
      }
      setHasCheckedAuth(true);
    }
  }, [user, loading, router]);

  // Show nothing or a loading spinner while checking auth status
  if (loading || !hasCheckedAuth) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0b0b12]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-theme-primary"></div>
      </div>
    );
  }

  // Unauthenticated user - show landing page
  return (
    <div className="min-h-screen bg-[#0b0b12] flex flex-col">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 border-b border-transparent border-b-[linear-gradient(90deg,_#ff2bd6,_#9c27b0,_#38bdf8)]">
        <div className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
          Todo App
        </div>
        <div>
          <Link href="/login">
            <span className="mr-4 text-[#e5e7eb] hover:text-[#38bdf8] cursor-pointer transition-colors neon-glow">Log in</span>
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-4 py-12 animate-fade-in">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
            Streamline Your Tasks, <br />
            <span className="text-[#38bdf8]">
              Boost Your Productivity
            </span>
          </h1>

          <p className="text-xl text-[#9ca3af] mb-10 max-w-2xl mx-auto neon-glow">
            Todo App helps you organize, prioritize, and complete your tasks efficiently.
            Join thousands of users who have transformed their productivity.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <button className="bg-[#ff2bd6] text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300 transform hover:scale-105">
                Get Started
              </button>
            </Link>

            <Link href="/login">
              <button className="bg-transparent border-2 border-[#00f5ff] text-[#00f5ff] px-8 py-4 text-lg font-semibold rounded-xl transition-all duration-300 hover:bg-[#00f5ff]/10">
                Sign In
              </button>
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-6 text-center text-[#9ca3af] text-sm neon-glow">
        © {new Date().getFullYear()} Todo App. All rights reserved.
      </footer>
    </div>
  );
}