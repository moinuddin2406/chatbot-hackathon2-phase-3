'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/auth-context';
import ThemeToggle from '../ui/theme-toggle';

interface NavigationProps {
  currentUser: { id: string; email: string; name?: string } | null;
  activePage: string;
  onLogout: () => void;
}

export default function Navigation({ currentUser, activePage, onLogout }: NavigationProps) {
  return (
    <header className="bg-[rgba(11,11,18,0.8)] backdrop-blur-md border-b border-transparent border-b-[linear-gradient(90deg,_#ff2bd6,_#9c27b0,_#38bdf8)]">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex flex-shrink-0 items-center">
              <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">
                Todo App
              </h1>
            </div>
            <nav className="ml-10 flex space-x-10">
              <Link
                href="/dashboard"
                className={`inline-flex items-center px-1 pt-1 text-base font-medium transition-all duration-300 ${
                  activePage === 'dashboard'
                    ? 'text-[#38bdf8] neon-glow'
                    : 'text-[#e5e7eb] hover:text-[#38bdf8] neon-glow'
                }`}
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className={`inline-flex items-center px-1 pt-1 text-base font-medium transition-all duration-300 ${
                  activePage === 'tasks'
                    ? 'text-[#38bdf8] neon-glow'
                    : 'text-[#e5e7eb] hover:text-[#38bdf8] neon-glow'
                }`}
              >
                Tasks
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            <div className="flex items-center space-x-6">
              <ThemeToggle />
              <div className="ml-3 relative">
                <div className="flex items-center space-x-6">
                  {currentUser && (
                    <span className="text-base text-[#e5e7eb] neon-glow">
                      Welcome, {currentUser.name || currentUser.email}
                    </span>
                  )}
                  <button
                    onClick={onLogout}
                    className="ml-4 text-base font-medium text-[#ff2bd6] hover:text-[#ff2bd6]/80 neon-glow transition-all duration-300"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}