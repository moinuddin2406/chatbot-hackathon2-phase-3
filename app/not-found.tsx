'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function NotFound() {
  const router = useRouter();

  // Optionally redirect to home after a delay
  useEffect(() => {
    const timer = setTimeout(() => {
      router.push('/');
    }, 3000); // Redirect after 3 seconds

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0b0b12] text-white">
      <h2 className="text-3xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8]">
        404 - Page Not Found
      </h2>
      <p className="text-lg mb-4 text-[#9ca3af]">
        The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
      </p>
      <p className="text-md mb-6 text-[#9ca3af]">
        Redirecting to homepage...
      </p>
      <button 
        onClick={() => router.push('/')}
        className="bg-[#ff2bd6] text-white px-6 py-3 rounded-xl shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300"
      >
        Go Home
      </button>
    </div>
  );
}