'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ui/protected-route';
import Navigation from '@/components/navigation/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import { normalizeTasksFromAPI, formatDate } from '@/utils/task-utils';

export default function DashboardPage() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [totalTasks, setTotalTasks] = useState(0);
  const [completedTasks, setCompletedTasks] = useState(0);
  const [pendingTasks, setPendingTasks] = useState(0);
  const [recentTasks, setRecentTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, [user]);

  const fetchDashboardData = async () => {
    if (!user?.id) return;

    try {
      setLoading(true);

      // Fetch all tasks for the user
      const response = await apiClient.get<any[]>(`/api/${user.id}/tasks`);
      const allTasks = normalizeTasksFromAPI(response);

      // Calculate metrics
      const total = allTasks.length;
      const completed = allTasks.filter(task => task.completed).length;
      const pending = allTasks.filter(task => !task.completed).length;
      const recent = allTasks.slice(0, 3); // Get the 3 most recent tasks

      setTotalTasks(total);
      setCompletedTasks(completed);
      setPendingTasks(pending);
      setRecentTasks(recent);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await signOut();
    router.push('/login');
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0b0b12]">
          <Navigation
            currentUser={user}
            activePage="dashboard"
            onLogout={handleLogout}
          />
          <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#38bdf8]"></div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0b0b12]">
        <Navigation
          currentUser={user}
          activePage="dashboard"
          onLogout={handleLogout}
        />

        <main className="pt-6 animate-fade-in">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="mb-10">
                <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow mb-2">Dashboard</h1>
                <p className="text-lg text-[#9ca3af] neon-glow">
                  Welcome back, {user?.name || user?.email}! Here's what's happening with your tasks today.
                </p>
              </div>

              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-10">
                {/* Summary cards with neon styling */}
                <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#38bdf8] backdrop-blur-md rounded-2xl p-6 shadow-[0_0_15px_#38bdf8] hover:shadow-[0_0_25px_#38bdf8] transition-all duration-300">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-8 w-8 text-[#38bdf8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dt className="text-sm font-medium text-[#9ca3af] neon-glow">Total Tasks</dt>
                      <dd className="text-3xl font-bold text-[#38bdf8] counter-animation">{totalTasks}</dd>
                    </div>
                  </div>
                </div>

                <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#00f5ff] backdrop-blur-md rounded-2xl p-6 shadow-[0_0_15px_#00f5ff] hover:shadow-[0_0_25px_#00f5ff] transition-all duration-300">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-8 w-8 text-[#00f5ff] fill-current" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dt className="text-sm font-medium text-[#9ca3af] neon-glow">Completed</dt>
                      <dd className="text-3xl font-bold text-[#00f5ff] counter-animation">{completedTasks}</dd>
                    </div>
                  </div>
                </div>

                <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#ff2bd6] backdrop-blur-md rounded-2xl p-6 shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-8 w-8 text-[#ff2bd6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dt className="text-sm font-medium text-[#9ca3af] neon-glow">Pending</dt>
                      <dd className="text-3xl font-bold text-[#ff2bd6] counter-animation">{pendingTasks}</dd>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mb-10">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-[#e5e7eb] neon-glow">Recent Tasks</h2>
                  <Link
                    href="/tasks"
                    className="text-sm font-medium text-[#38bdf8] hover:text-[#38bdf8]/80 transition-colors neon-glow"
                  >
                    View all
                  </Link>
                </div>

                <div className="space-y-4">
                  {recentTasks.length > 0 ? (
                    recentTasks.map((task) => (
                      <div
                        key={task.id}
                        className={`bg-[rgba(20,20,30,0.85)] backdrop-blur-md rounded-2xl p-5 transition-all duration-300 hover:scale-[1.02] ${
                          task.completed
                            ? 'border-2 border-[#00ff9d] shadow-[0_0_15px_#00ff9d]'
                            : 'border-2 border-[#38bdf8] shadow-[0_0_15px_#38bdf8]'
                        }`}
                      >
                        <div className="flex items-start">
                          <input
                            type="checkbox"
                            checked={task.completed}
                            readOnly
                            className="h-5 w-5 mt-0.5 rounded border-[#38bdf8] text-[#ff2bd6] focus:ring-[#ff2bd6] focus:ring-offset-0 focus:ring-2 focus:ring-offset-2 focus:ring-[#ff2bd6]"
                          />
                          <div className="ml-3 flex-1 min-w-0">
                            <div className={`text-base font-semibold truncate ${task.completed ? 'text-[#00ff9d] line-through' : 'text-[#e5e7eb] hover:text-[#38bdf8]'}`}>
                              {task.title}
                            </div>
                            <div className="mt-2 flex items-center text-sm text-[#9ca3af]">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-[#9ca3af]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                              <span>Due: {formatDate(task.due_date)}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#38bdf8] backdrop-blur-md rounded-2xl p-6 text-center shadow-[0_0_15px_#38bdf8]">
                      <p className="text-[#9ca3af] neon-glow">No recent tasks. Create your first task!</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="text-center mb-10">
                <Link
                  href="/tasks/new"
                  className="bg-[#ff2bd6] text-white px-6 py-3 text-base font-semibold rounded-xl shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300 transform hover:scale-105"
                >
                  Create New Task
                </Link>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}