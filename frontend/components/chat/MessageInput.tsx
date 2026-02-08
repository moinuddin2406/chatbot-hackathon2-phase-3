import React, { useState } from 'react';

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSend, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={!message.trim() || disabled}
        className={`px-4 py-2 rounded-r-lg text-white ${
          message.trim() && !disabled
            ? 'bg-blue-600 hover:bg-blue-700'
            : 'bg-blue-400 cursor-not-allowed'
        }`}
      >
        Send
      </button>
    </form>
  );
};

export default MessageInput;