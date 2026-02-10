import { apiClient } from './api';
import { Task } from './types';
import { normalizeTaskFromAPI, normalizeTasksFromAPI } from '@/utils/task-utils';

// Service functions that encapsulate task operations
// These are the same functions used by both UI components and chatbot

export const taskService = {
  // Get all tasks for a user
  async getAllTasks(userId: string): Promise<Task[]> {
    try {
      const response = await apiClient.get<any[]>(`/api/${userId}/tasks`);
      return normalizeTasksFromAPI(response);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
      throw error;
    }
  },

  // Add a new task
  async addTask(userId: string, taskData: { title: string; description?: string }): Promise<Task> {
    try {
      const response = await apiClient.post<any>(`/api/${userId}/tasks`, taskData);
      return normalizeTaskFromAPI(response);
    } catch (error) {
      console.error('Failed to add task:', error);
      throw error;
    }
  },

  // Update an existing task
  async updateTask(userId: string, taskId: string, taskData: Partial<{ title: string; description?: string; completed?: boolean }>): Promise<Task> {
    try {
      const response = await apiClient.put<any>(`/api/${userId}/tasks/${taskId}`, taskData);
      return normalizeTaskFromAPI(response);
    } catch (error) {
      console.error('Failed to update task:', error);
      throw error;
    }
  },

  // Delete a task
  async deleteTask(userId: string, taskId: string): Promise<void> {
    try {
      await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    } catch (error) {
      console.error('Failed to delete task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleTaskCompletion(userId: string, taskId: string): Promise<Task> {
    try {
      const response = await apiClient.patch<any>(`/api/${userId}/tasks/${taskId}/complete`, {});
      return normalizeTaskFromAPI(response);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
      throw error;
    }
  }
};