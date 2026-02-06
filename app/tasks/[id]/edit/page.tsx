'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter, useParams } from 'next/navigation';
import ProtectedRoute from '@/components/ui/protected-route';
import Navigation from '@/components/navigation/navigation';
import TaskForm from '@/components/tasks/task-form';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';

export default function EditTaskPage() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState<Record<string, string>>({});

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
      const normalizedTask = {
        ...response,
        due_date: response.due_date || null,
      };
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

  const handleSubmit = async (taskData: Task) => {
    setLoading(true);
    setErrors({});

    try {
      // Check if user is authenticated before making the API call
      if (!user?.id) {
        console.error('User not authenticated');
        setErrors({ general: 'User not authenticated. Please log in.' });
        return;
      }

      // Update the task via the backend API - note the user ID in the URL path
      // Send all required fields for task update (title, description, completed, due_date)
      const taskPayload = {
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed,
        due_date: taskData.due_date || null
      };
      const response = await apiClient.put<any>(`/api/${user.id}/tasks/${taskId}`, taskPayload);

      // Navigate back to tasks page after successful update
      router.push('/tasks');
      router.refresh();
    } catch (error: any) {
      console.error('Failed to update task:', error);
      if (error.response?.data?.errors) {
        setErrors(error.response.data.errors);
      } else {
        setErrors({ general: 'Failed to update task. Please try again.' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
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
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-theme-text-primary neon-text-gradient">Edit Task</h1>
              </div>

              {errors.general && (
                <div className="mb-4 neon-card p-4 rounded-lg">
                  <div className="text-theme-danger text-sm neon-glow">{errors.general}</div>
                </div>
              )}

              <TaskForm
                task={task}
                onSubmit={handleSubmit}
                onCancel={handleCancel}
                isLoading={loading}
                errors={errors}
              />
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}