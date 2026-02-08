import React, { useState, useEffect, useRef } from 'react';
import MessageDisplay from './MessageDisplay';
import MessageInput from './MessageInput';
import LoadingIndicator from './LoadingIndicator';
import ErrorDisplay from './ErrorDisplay';
import { FaTimes } from 'react-icons/fa';

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
  messages: Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>;
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  errorMessage?: string;
}

const ChatPanel: React.FC<ChatPanelProps> = ({
  isOpen,
  onClose,
  messages,
  onSendMessage,
  isLoading,
  errorMessage
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = (message: string) => {
    onSendMessage(message);
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div 
      className="fixed bottom-24 right-6 w-full max-w-md h-[70vh] flex flex-col bg-white border border-gray-300 rounded-lg shadow-xl z-[9998]"
      onClick={(e) => e.stopPropagation()}
    >
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h2 className="text-lg font-semibold">Chat Assistant</h2>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
          className="text-white hover:text-gray-200 focus:outline-none"
          aria-label="Close chat"
        >
          <FaTimes />
        </button>
      </div>

      {/* Messages Container */}
      <div 
        className="flex-1 overflow-y-auto p-4 bg-gray-50"
        onClick={(e) => e.stopPropagation()}
      >
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation with the assistant...</p>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <MessageDisplay
                key={msg.id}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />
            ))}
            {isLoading && <LoadingIndicator />}
            <div ref={messagesEndRef} />
          </>
        )}

        {errorMessage && <ErrorDisplay message={errorMessage} />}
      </div>

      {/* Input Area */}
      <div 
        className="border-t border-gray-300 p-4 bg-white"
        onClick={(e) => e.stopPropagation()}
      >
        <MessageInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatPanel;