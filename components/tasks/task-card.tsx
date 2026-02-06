import React from 'react';
import { formatDateOnly, formatDateTime } from '@/utils/date-utils';
import { formatDate } from '@/utils/task-utils';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  due_date?: string | null;
  updated_at: string;
  user_id: string;
}

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: string) => void;
  onEdit: (taskId: string) => void;
  onDelete: (taskId: string) => void;
  onSelect: (taskId: string) => void;
}

export default function TaskCard({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
  onSelect
}: TaskCardProps) {

  return (
    <div
      className={`rounded-2xl p-5 transition-all duration-300 hover:scale-[1.02] slide-in ${
        task.completed
          ? 'border-2 border-[var(--color-success)] shadow-[var(--neon-glow)] hover:shadow-[var(--neon-glow-intense)]'
          : 'border-2 border-[var(--color-primary)] shadow-[var(--neon-glow)] hover:shadow-[var(--neon-glow-intense)]'
      }`}
      style={{
        background: 'var(--color-card-bg)',
        backdropFilter: 'var(--glassmorphism, none)',
        WebkitBackdropFilter: 'var(--glassmorphism, none)',
      }}
    >
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task.id)}
          className="h-5 w-5 mt-0.5 rounded border-[var(--color-primary)] text-[var(--color-primary)] focus:ring-[var(--color-primary)] focus:ring-offset-0 focus:ring-2 focus:ring-offset-2 focus:ring-[var(--color-primary)] transition-all duration-300"
        />
        <div className="ml-3 flex-1 min-w-0">
          <div
            className={`text-base font-semibold truncate cursor-pointer transition-all duration-300 ${
              task.completed ? 'text-[var(--color-success)] line-through' : 'text-[var(--color-text-primary)] hover:text-[var(--color-primary)]'
            }`}
            onClick={() => onSelect(task.id)}
          >
            {task.title}
          </div>
          {task.description && (
            <p className={`text-sm mt-1 truncate transition-all duration-300 ${task.completed ? 'text-[var(--color-success)]/70' : 'text-[var(--color-text-secondary)]'}`}>
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className={`text-xs transition-all duration-300 ${task.completed ? 'text-[var(--color-success)]/70' : 'text-[var(--color-text-secondary)]'}`}>
              Due: {formatDate(task.due_date)}
            </span>
          </div>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-[var(--color-text-secondary)]/60 transition-all duration-300">Created: {formatDate(task.created_at)}</span>
            </div>
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span className="text-[var(--color-text-secondary)]/60 transition-all duration-300">Updated: {formatDate(task.updated_at)}</span>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-4 flex justify-end space-x-3 pt-2 border-t border-[var(--color-primary)]/30 transition-all duration-300">
        <button
          onClick={() => onEdit(task.id)}
          className="bg-transparent border border-[var(--color-accent)] text-[var(--color-accent)] text-sm font-medium px-3 py-1.5 rounded-lg transition-all duration-300 hover:bg-[var(--color-accent)]/10 hover:scale-105"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="bg-transparent border border-[var(--color-danger)] text-[var(--color-danger)] text-sm font-medium px-3 py-1.5 rounded-lg transition-all duration-300 hover:bg-[var(--color-danger)]/10 hover:scale-105"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete
        </button>
      </div>
    </div>
  );
}