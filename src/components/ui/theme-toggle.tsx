'use client';

import React from 'react';
import { useTheme } from '@/context/theme-context';

const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-[#9ca3af] neon-glow">Theme:</span>
      <div className="flex flex-wrap gap-1 bg-[rgba(20,20,30,0.6)] p-1 rounded-lg">
        <button
          onClick={() => setTheme('light')}
          className={`px-2 py-1 text-xs rounded-md transition-colors min-w-[50px] ${
            theme === 'light'
              ? 'bg-[#ff2bd6] text-white shadow-[0_0_8px_#ff2bd6]'
              : 'text-[#e5e7eb] hover:bg-[rgba(20,20,30,0.8)]'
          }`}
          aria-label="Light theme"
        >
          Light
        </button>
        <button
          onClick={() => setTheme('dark')}
          className={`px-2 py-1 text-xs rounded-md transition-colors min-w-[50px] ${
            theme === 'dark'
              ? 'bg-[#ff2bd6] text-white shadow-[0_0_8px_#ff2bd6]'
              : 'text-[#e5e7eb] hover:bg-[rgba(20,20,30,0.8)]'
          }`}
          aria-label="Dark theme"
        >
          Dark
        </button>
        <button
          onClick={() => setTheme('emerald')}
          className={`px-2 py-1 text-xs rounded-md transition-colors min-w-[50px] ${
            theme === 'emerald'
              ? 'bg-[#ff2bd6] text-white shadow-[0_0_8px_#ff2bd6]'
              : 'text-[#e5e7eb] hover:bg-[rgba(20,20,30,0.8)]'
          }`}
          aria-label="Emerald theme"
        >
          Emerald
        </button>
        <button
          onClick={() => setTheme('neon-cyberpunk')}
          className={`px-2 py-1 text-xs rounded-md transition-colors min-w-[50px] ${
            theme === 'neon-cyberpunk'
              ? 'bg-[#ff2bd6] text-white shadow-[0_0_8px_#ff2bd6]'
              : 'text-[#e5e7eb] hover:bg-[rgba(20,20,30,0.8)]'
          }`}
          aria-label="Neon Cyberpunk theme"
        >
          Neon
        </button>
      </div>
    </div>
  );
};

export default ThemeToggle;