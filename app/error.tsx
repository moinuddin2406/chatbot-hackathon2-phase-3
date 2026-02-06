'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const router = useRouter();

  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Global error caught:', error);
  }, [error]);

  return (
    <html>
      <body className="bg-[#0b0b12] flex flex-col items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8]">
            Something went wrong!
          </h2>
          <p className="text-lg mb-4 text-[#9ca3af]">
            An unexpected error has occurred.
          </p>
          <div className="mb-6 p-4 bg-red-900/30 rounded-lg text-left overflow-auto max-w-md">
            <pre className="text-sm text-red-300">
              {error.message || 'Unknown error'}
            </pre>
          </div>
          <div className="space-y-4">
            <button
              onClick={() => reset()}
              className="bg-[#38bdf8] text-white px-6 py-3 rounded-xl mr-4 shadow-[0_0_15px_#38bdf8] hover:shadow-[0_0_25px_#38bdf8] transition-all duration-300"
            >
              Try Again
            </button>
            <button
              onClick={() => router.push('/')}
              className="bg-[#ff2bd6] text-white px-6 py-3 rounded-xl shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300"
            >
              Go Home
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}