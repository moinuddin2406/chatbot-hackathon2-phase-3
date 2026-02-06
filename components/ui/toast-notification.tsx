import React, { useEffect } from 'react';

interface ToastNotificationProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onDismiss?: () => void;
}

export default function ToastNotification({ 
  message, 
  type = 'info', 
  duration = 5000, 
  onDismiss 
}: ToastNotificationProps) {
  const typeStyles = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500',
  };

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onDismiss && onDismiss();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onDismiss]);

  return (
    <div className={`fixed top-4 right-4 ${typeStyles[type]} text-white px-4 py-2 rounded-md shadow-lg z-50 flex items-center`}>
      <span>{message}</span>
      {onDismiss && (
        <button 
          onClick={onDismiss} 
          className="ml-4 text-white focus:outline-none"
        >
          &times;
        </button>
      )}
    </div>
  );
}