// src/utils/task-utils.ts
// Utility functions for task normalization and processing

import { Task, User } from '@/lib/types';

/**
 * Normalize task object from API response (snake_case) to camelCase
 */
export function normalizeTaskFromAPI(apiTask: any): Task {
  return {
    id: String(apiTask.id),
    title: apiTask.title,
    description: apiTask.description,
    completed: apiTask.completed,
    created_at: apiTask.created_at,
    due_date: apiTask.due_date || null,
    updated_at: apiTask.updated_at,
    user_id: apiTask.user_id,
  };
}

/**
 * Normalize array of task objects from API response (snake_case) to camelCase
 */
export function normalizeTasksFromAPI(apiTasks: any[]): Task[] {
  return apiTasks.map(normalizeTaskFromAPI);
}

/**
 * Normalize user object from API response (snake_case) to camelCase
 */
export function normalizeUserFromAPI(apiUser: any): User {
  return {
    id: apiUser.id,
    email: apiUser.email,
    name: apiUser.name,
    created_at: apiUser.created_at,
    updated_at: apiUser.updated_at,
  };
}

/**
 * Format date values consistently
 */
export function formatDate(value: string | null | undefined): string {
  if (!value) return "—";
  const d = new Date(value);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleDateString();
}