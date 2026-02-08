import React from 'react';

interface ErrorDisplayProps {
  message: string;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ message }) => {
  return (
    <div className="mt-2 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
      <span className="font-bold">Error:</span> {message}
    </div>
  );
};

export default ErrorDisplay;