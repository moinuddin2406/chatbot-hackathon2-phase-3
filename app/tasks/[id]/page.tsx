'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter, useParams } from 'next/navigation';
import ProtectedRoute from '@/components/ui/protected-route';
import Navigation from '@/components/navigation/navigation';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import { normalizeTaskFromAPI, formatDate } from '@/utils/task-utils';

export default function ViewTaskPage() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTask();
  }, []);

  const fetchTask = async () => {
    try {
      setLoading(true);

      // Check if user is authenticated before making the API call
      if (!user?.id) {
        console.error('User not authenticated');
        router.push('/login'); // Redirect to login if not authenticated
        return;
      }

      // Fetch the task from the backend API - note the user ID in the URL path
      const response = await apiClient.get<any>(`/api/${user.id}/tasks/${taskId}`);
      const normalizedTask = normalizeTaskFromAPI(response);
      setTask(normalizedTask);
    } catch (error) {
      console.error('Failed to fetch task:', error);
      router.push('/tasks'); // Redirect if task doesn't exist
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await signOut();
    router.push('/login');
  };

  const handleEdit = () => {
    router.push(`/tasks/${taskId}/edit`);
  };

  const handleDelete = async () => {
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

      // Navigate back to tasks page after successful deletion
      router.push('/tasks');
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleBack = () => {
    router.push('/tasks');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-theme-primary"></div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-theme-text-secondary neon-glow">Task not found</div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-theme-background">
        <Navigation
          currentUser={user}
          activePage="tasks"
          onLogout={handleLogout}
        />

        <main className="animate-fade-in">
          <div className="mx-auto max-w-2xl py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="mb-6 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-theme-text-primary neon-text-gradient">Task Details</h1>
                <button
                  onClick={handleBack}
                  className="text-theme-primary hover:text-theme-primary-hover transition-colors neon-glow"
                >
                  Back to Tasks
                </button>
              </div>

              <div className="neon-card p-6 rounded-2xl">
                <div className="flex items-start mb-4">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => {}}
                    disabled
                    className="h-5 w-5 mt-1 rounded border-theme-secondary text-theme-primary focus:ring-theme-primary"
                  />
                  <div className="ml-3 flex-1">
                    <h2 className={`text-xl font-semibold ${
                      task.completed ? 'text-theme-success line-through neon-glow-green' : 'text-theme-text-primary neon-glow'
                    }`}>
                      {task.title}
                    </h2>
                  </div>
                </div>

                {task.description && (
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-theme-text-secondary mb-1 neon-glow">Description</h3>
                    <p className="text-theme-text-primary neon-glow">{task.description}</p>
                  </div>
                )}

                <div className="mb-4">
                  <h3 className="text-sm font-medium text-theme-text-secondary mb-1 neon-glow">Due Date</h3>
                  <p className="text-theme-text-primary neon-glow">{formatDate(task.due_date)}</p>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <h3 className="text-sm font-medium text-theme-text-secondary mb-1 neon-glow">Created</h3>
                    <p className="text-theme-text-primary neon-glow">{formatDate(task.created_at)}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-theme-text-secondary mb-1 neon-glow">Updated</h3>
                    <p className="text-theme-text-primary neon-glow">{formatDate(task.updated_at)}</p>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={handleEdit}
                    className="neon-button flex-1 px-4 py-2 text-sm font-semibold shadow-lg hover:shadow-xl transition-all duration-300 rounded-lg"
                  >
                    Edit Task
                  </button>
                  <button
                    onClick={handleDelete}
                    className="neon-button-secondary flex-1 px-4 py-2 text-sm font-semibold transition-all duration-300 rounded-lg"
                  >
                    Delete Task
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}