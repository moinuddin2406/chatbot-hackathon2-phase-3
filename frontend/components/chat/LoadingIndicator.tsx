import React from 'react';

interface LoadingIndicatorProps {
  message?: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ message = 'Thinking...' }) => {
  return (
    <div className="flex items-center justify-start mb-4">
      <div className="bg-gray-200 text-gray-800 rounded-lg rounded-bl-none px-4 py-2">
        <div className="flex items-center">
          <div className="mr-2">{message}</div>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;