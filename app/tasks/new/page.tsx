'use client';

import React, { useState } from 'react';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ui/protected-route';
import Navigation from '@/components/navigation/navigation';
import TaskForm from '@/components/tasks/task-form';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';

export default function NewTaskPage() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

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

      // Create the task via the backend API - note the user ID in the URL path
      // Send all required fields for task creation (title, description, completed, due_date)
      const taskPayload = {
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed || false,
        due_date: taskData.due_date || null
      };
      const response = await apiClient.post<any>(`/api/${user.id}/tasks`, taskPayload);

      // Navigate back to tasks page after successful creation
      router.push('/tasks');
      router.refresh();
    } catch (error: any) {
      console.error('Failed to create task:', error);
      if (error.response?.data?.errors) {
        setErrors(error.response.data.errors);
      } else {
        setErrors({ general: 'Failed to create task. Please try again.' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

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
                <h1 className="text-2xl font-bold text-theme-text-primary neon-text-gradient">Create New Task</h1>
              </div>

              {errors.general && (
                <div className="mb-4 neon-card p-4 rounded-lg">
                  <div className="text-theme-danger text-sm neon-glow">{errors.general}</div>
                </div>
              )}

              <TaskForm
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