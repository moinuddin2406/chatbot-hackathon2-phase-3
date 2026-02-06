'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ui/protected-route';
import Navigation from '@/components/navigation/navigation';
import TaskCard from '@/components/tasks/task-card';
import EmptyState from '@/components/ui/empty-state';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import { normalizeTaskFromAPI, normalizeTasksFromAPI, formatDate } from '@/utils/task-utils';

export default function TasksPage() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'priority'>('date');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, [user?.id]); // Add user.id as dependency to refetch when user changes

  useEffect(() => {
    filterAndSortTasks();
  }, [tasks, filter, sortBy]);

  const fetchTasks = async () => {
    try {
      setLoading(true);

      // Check if user is authenticated before making the API call
      if (!user?.id) {
        console.error('User not authenticated');
        return;
      }

      // Fetch from the backend API - note the user ID in the URL path
      const response = await apiClient.get<any[]>(`/api/${user.id}/tasks`);
      const normalizedTasks = normalizeTasksFromAPI(response);
      setTasks(normalizedTasks);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterAndSortTasks = () => {
    let result = [...tasks];

    // Apply filter
    if (filter === 'completed') {
      result = result.filter(task => task.completed);
    } else if (filter === 'pending') {
      result = result.filter(task => !task.completed);
    }

    // Apply sort
    if (sortBy === 'date') {
      result.sort((a, b) => new Date(a.due_date || a.created_at).getTime() - new Date(b.due_date || b.created_at).getTime());
    }
    // Priority sorting would be implemented here if priorities were available

    setFilteredTasks(result);
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      // Check if user is authenticated before making the API call
      if (!user?.id) {
        console.error('User not authenticated');
        return;
      }

      // Update the task via the backend API
      const response = await apiClient.patch<any>(`/api/${user.id}/tasks/${taskId}/complete`, {});
      const normalizedTask = normalizeTaskFromAPI(response);

      // Update the local state with the response
      setTasks(tasks.map(task =>
        task.id === taskId ? normalizedTask : task
      ));
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleEdit = (taskId: string) => {
    router.push(`/tasks/${taskId}/edit`);
  };

  const handleDelete = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      // Check if user is authenticated before making the API call
      if (!user?.id) {
        console.error('User not authenticated');
        return;
      }

      // Delete the task via the backend API
      await apiClient.delete(`/api/${user.id}/tasks/${taskId}`);

      // Update the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleSelect = (taskId: string) => {
    router.push(`/tasks/${taskId}`); // Navigate to view task details
  };

  const handleLogout = async () => {
    await signOut();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-theme-primary"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0b0b12]">
        <Navigation
          currentUser={user}
          activePage="tasks"
          onLogout={handleLogout}
        />

        <main className="pt-6 animate-fade-in">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="mb-8">
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#3bdcff] to-[#38bdf8] neon-glow">Tasks</h1>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 space-y-4 sm:space-y-0">
                <div className="flex flex-wrap gap-4">
                  <div>
                    <label htmlFor="filter" className="block text-sm font-medium text-[#9ca3af] mb-1 neon-glow">
                      Filter
                    </label>
                    <select
                      id="filter"
                      value={filter}
                      onChange={(e) => setFilter(e.target.value as 'all' | 'completed' | 'pending')}
                      className="bg-[rgba(20,20,30,0.6)] border border-[#00f5ff] text-[#e5e7eb] py-2 px-3 rounded-lg min-w-[140px] focus:outline-none focus:ring-2 focus:ring-[#00f5ff] focus:border-transparent shadow-[inset_0_0_5px_rgba(0,245,255,0.3)]"
                    >
                      <option value="all">All Tasks</option>
                      <option value="completed">Completed</option>
                      <option value="pending">Pending</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="sort" className="block text-sm font-medium text-[#9ca3af] mb-1 neon-glow">
                      Sort By
                    </label>
                    <select
                      id="sort"
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value as 'date' | 'priority')}
                      className="bg-[rgba(20,20,30,0.6)] border border-[#00f5ff] text-[#e5e7eb] py-2 px-3 rounded-lg min-w-[140px] focus:outline-none focus:ring-2 focus:ring-[#00f5ff] focus:border-transparent shadow-[inset_0_0_5px_rgba(0,245,255,0.3)]"
                    >
                      <option value="date">Due Date</option>
                      <option value="priority">Priority</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={() => router.push('/tasks/new')}
                  className="bg-[#ff2bd6] text-white inline-flex items-center px-4 py-2.5 text-sm font-semibold rounded-lg shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300 whitespace-nowrap transform hover:scale-105"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Create New Task
                </button>
              </div>

              {filteredTasks.length === 0 ? (
                <div className="bg-[rgba(20,20,30,0.85)] border-2 border-[#38bdf8] backdrop-blur-md text-center p-12 rounded-2xl shadow-[0_0_15px_#38bdf8]">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-12 w-12 text-[#9ca3af]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="mt-2 text-lg font-medium text-[#e5e7eb] neon-glow">No tasks</h3>
                  <p className="mt-1 text-base text-[#9ca3af] neon-glow">
                    {filter !== 'all'
                      ? `No ${filter} tasks found.`
                      : "Get started by creating a new task."}
                  </p>
                  <div className="mt-6">
                    <button
                      onClick={() => router.push('/tasks/new')}
                      className="bg-[#ff2bd6] text-white inline-flex items-center px-4 py-2.5 text-sm font-semibold rounded-lg shadow-[0_0_15px_#ff2bd6] hover:shadow-[0_0_25px_#ff2bd6] transition-all duration-300 transform hover:scale-105"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Create New Task
                    </button>
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                  {filteredTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onToggleComplete={handleToggleComplete}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                      onSelect={handleSelect}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}