'use client';

import React, { useEffect } from 'react';
import { useChat } from '@/frontend/context/ChatContext';
import { useAuth } from '@/context/auth-context';
import FloatingChatIcon from '@/frontend/components/chat/FloatingChatIcon';
import ChatPanel from '@/frontend/components/chat/ChatPanel';
import { apiClient } from '@/lib/api';
import { taskService } from '@/lib/task-service';

const ChatIntegration: React.FC = () => {
  const { state, setOpen, addMessage, setLoading, setError, triggerTaskUpdate } = useChat();
  const { user } = useAuth();

  const toggleChat = () => {
    setOpen(!state.isOpen);
  };

  const handleSendMessage = async (message: string) => {
    if (!user?.id) {
      setError('User not authenticated. Please log in first.');
      addMessage({
        role: 'assistant',
        content: 'You need to be logged in to use the chatbot. Please log in first.',
        timestamp: new Date(),
      });
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Add user message
      addMessage({
        role: 'user',
        content: message,
        timestamp: new Date(),
      });

      // Call the backend API to get AI response
      // The API expects the user ID in the path: /api/{user_id}/chat (based on OpenAPI spec)
      const response = await apiClient.post(`/api/${user.id}/chat`, { message });

      // Type assertion for the response to access properties safely
      const responseData = response as { response?: string; tool_calls?: any[] };

      // Add AI response
      addMessage({
        role: 'assistant',
        content: responseData.response || 'Sorry, I could not process your request.',
        timestamp: new Date(),
      });

      // Check if the response includes tool calls that affect tasks
      if (responseData.tool_calls && Array.isArray(responseData.tool_calls)) {
        // Check if any of the tool calls were task-related operations
        const taskOperations = responseData.tool_calls.filter((call: any) =>
          call && call.name && ['add_task', 'update_task', 'delete_task', 'complete_task'].includes(call.name)
        );

        if (taskOperations.length > 0) {
          // Trigger UI update to refresh the task list
          triggerTaskUpdate();
        }
      }
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Determine the appropriate error message based on the error type
      let errorMessage = 'Sorry, I\'m having trouble processing your request right now.';
      
      if (error.message?.includes('401')) {
        errorMessage = 'Authentication error. Please log in again.';
      } else if (error.message?.includes('Network error')) {
        errorMessage = 'Unable to connect to the server. Please check your connection.';
      } else if (error.message) {
        errorMessage += ` Error: ${error.message}`;
      }

      // Add an error message to the chat instead of just setting state error
      addMessage({
        role: 'assistant',
        content: errorMessage,
        timestamp: new Date(),
      });

      // Still set the error state for UI purposes
      setError(`Failed to get response from the AI service: ${error.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  // Close chat when pressing Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && state.isOpen) {
        setOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [state.isOpen, setOpen]);

  return (
    <>
      <FloatingChatIcon onToggleChat={toggleChat} />
      <ChatPanel
        isOpen={state.isOpen}
        onClose={() => setOpen(false)}
        messages={state.messages}
        onSendMessage={handleSendMessage}
        isLoading={state.isLoading}
        errorMessage={state.error || undefined}
      />
    </>
  );
};

export default ChatIntegration;