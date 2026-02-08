import React from 'react';
import { FaComment } from 'react-icons/fa';

interface FloatingChatIconProps {
  onToggleChat: () => void;
}

const FloatingChatIcon: React.FC<FloatingChatIconProps> = ({ onToggleChat }) => {
  return (
    <div className="fixed bottom-6 right-6 z-[9999]">
      <button
        onClick={(e) => {
          e.stopPropagation();
          onToggleChat();
        }}
        className="bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        aria-label="Open chat"
      >
        <FaComment size={20} />
      </button>
    </div>
  );
};

export default FloatingChatIcon;