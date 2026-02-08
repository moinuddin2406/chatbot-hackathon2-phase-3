export interface ChatRequest {
  conversation_id?: string;
  message: string;
}

export interface ToolCallResult {
  name: string;
  arguments: Record<string, any>;
  result?: any;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: ToolCallResult[];
}

export interface Message {
  id: string;
  conversation_id: string;
  user_id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: any;
  created_at: string;
}