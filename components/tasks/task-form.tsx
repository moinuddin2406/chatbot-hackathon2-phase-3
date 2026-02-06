import React, { useState, useEffect } from 'react';

interface Task {
  id?: string;
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: string | null;
}

interface TaskFormProps {
  task?: Task;
  onSubmit: (taskData: any) => void; // Will submit in snake_case format
  onCancel: () => void;
  isLoading: boolean;
  errors?: Record<string, string>;
}

export default function TaskForm({
  task,
  onSubmit,
  onCancel,
  isLoading,
  errors = {}
}: TaskFormProps) {
  const [formData, setFormData] = useState<Task>({
    title: '',
    description: '',
    due_date: null,
    completed: false,
    ...task,
  });

  useEffect(() => {
    setFormData({
      title: '',
      description: '',
      due_date: null,
      completed: false,
      ...task,
    });
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    // Map camelCase field names to snake_case for API compatibility
    const fieldName = name === 'dueDate' ? 'due_date' : name;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

    setFormData(prev => ({
      ...prev,
      [fieldName]: val
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Convert camelCase to snake_case for API submission
    const apiTaskData = {
      ...formData,
      due_date: formData.due_date || undefined, // Use undefined instead of null for API
    };
    onSubmit(apiTaskData);
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-theme-text-primary mb-1 neon-glow">
            Title *
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="title"
              id="title"
              required
              value={formData.title}
              onChange={handleChange}
              disabled={isLoading}
              className={`block w-full neon-input py-3 px-4 text-theme-text-primary rounded-lg transition-colors ${
                errors.title ? 'ring-theme-danger' : ''
              }`}
            />
            {errors.title && <p className="mt-1 text-sm text-theme-danger neon-glow">{errors.title}</p>}
          </div>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-theme-text-primary mb-1 neon-glow">
            Description
          </label>
          <div className="mt-1">
            <textarea
              name="description"
              id="description"
              rows={4}
              value={formData.description || ''}
              onChange={handleChange}
              disabled={isLoading}
              className="block w-full neon-input py-3 px-4 text-theme-text-primary rounded-lg transition-colors"
            />
          </div>
        </div>

        <div>
          <label htmlFor="dueDate" className="block text-sm font-medium text-theme-text-primary mb-1 neon-glow">
            Due Date
          </label>
          <div className="mt-1">
            <input
              type="date"
              name="dueDate"
              id="dueDate"
              value={formData.due_date || ''}
              onChange={handleChange}
              disabled={isLoading}
              className="block w-full neon-input py-3 px-4 text-theme-text-primary rounded-lg transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center pt-2">
          <input
            id="completed"
            name="completed"
            type="checkbox"
            checked={formData.completed || false}
            onChange={handleChange}
            disabled={isLoading}
            className="h-5 w-5 rounded border-theme-card-border text-theme-primary focus:ring-theme-primary focus:ring-2 focus:ring-offset-2 focus:ring-theme-primary"
          />
          <label htmlFor="completed" className="ml-2 block text-sm text-theme-text-primary neon-glow">
            Mark as completed
          </label>
        </div>

        <div className="flex flex-col sm:flex-row sm:space-x-4 space-y-3 sm:space-y-0 pt-6">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 neon-button px-4 py-3 text-sm font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : task?.id ? (
              'Update Task'
            ) : (
              'Create Task'
            )}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="flex-1 neon-button-secondary px-4 py-3 text-sm font-semibold transition-all duration-300"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}