import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Define types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  isOpen: boolean;
}

type ChatAction =
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_OPEN'; payload: boolean }
  | { type: 'CLEAR_MESSAGES' };

// Initial state
const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  isOpen: false,
};

// Reducer
const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
        error: null,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    case 'SET_OPEN':
      return {
        ...state,
        isOpen: action.payload,
      };
    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
      };
    default:
      return state;
  }
};

// Create context
interface ChatContextType {
  state: ChatState;
  addMessage: (message: Omit<Message, 'id'>) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setOpen: (open: boolean) => void;
  clearMessages: () => void;
  triggerTaskUpdate: () => void; // Function to trigger UI updates
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
interface ChatProviderProps {
  children: ReactNode;
}

// Global callback to trigger UI updates (will be set by the TasksPage)
let triggerTaskUpdateCallback: (() => void) | null = null;

export const setTriggerTaskUpdateCallback = (callback: () => void) => {
  triggerTaskUpdateCallback = callback;
};

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const addMessage = (messageWithoutId: Omit<Message, 'id'>) => {
    const message: Message = {
      ...messageWithoutId,
      id: Date.now().toString(),
    };
    dispatch({ type: 'ADD_MESSAGE', payload: message });
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const setError = (error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  const setOpen = (open: boolean) => {
    dispatch({ type: 'SET_OPEN', payload: open });
  };

  const clearMessages = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
  };

  const triggerTaskUpdate = () => {
    if (triggerTaskUpdateCallback) {
      triggerTaskUpdateCallback();
    }
  };

  const value = {
    state,
    addMessage,
    setLoading,
    setError,
    setOpen,
    clearMessages,
    triggerTaskUpdate,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Hook to use the context
export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};