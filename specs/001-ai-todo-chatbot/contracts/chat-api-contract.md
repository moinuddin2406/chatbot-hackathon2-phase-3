# API Contract: Chat Endpoint

## Endpoint
```
POST /api/{user_id}/chat
```

## Description
Handles chat interactions between the user and the AI assistant. Processes natural language input, manages conversation context, and orchestrates tool calls as needed.

## Request

### Path Parameters
- `user_id` (string, required)
  - The unique identifier of the user making the request
  - Used to scope all operations to the correct user

### Request Body
```json
{
  "conversation_id": "string (optional)",
  "message": "string (required)"
}
```

#### Fields
- `conversation_id` (optional)
  - Unique identifier of an existing conversation
  - If omitted, a new conversation will be created
  - Format: UUID string

- `message` (required)
  - The natural language message from the user
  - Will be processed by the AI agent to determine intent
  - Type: String
  - Min length: 1 character

## Response

### Success Response (200 OK)
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": "array (optional)"
}
```

#### Fields
- `conversation_id` (required)
  - The identifier of the conversation (existing or newly created)
  - Format: UUID string

- `response` (required)
  - The AI-generated response to the user's message
  - Type: String

- `tool_calls` (optional)
  - Array of tool calls that were executed as part of processing the message
  - May be omitted if no tools were called
  - Format: Array of tool call objects

### Tool Call Object Format
```json
{
  "name": "string",
  "arguments": "object",
  "result": "object (optional)"
}
```

#### Fields
- `name` (required)
  - The name of the tool that was called
  - Examples: "add_task", "list_tasks", "complete_task", etc.

- `arguments` (required)
  - The arguments that were passed to the tool
  - Format: Object with parameter names as keys

- `result` (optional)
  - The result returned by the tool execution
  - May be omitted if the tool is still executing or failed

### Error Response (4xx/5xx)
```json
{
  "error": "string",
  "code": "string"
}
```

#### Fields
- `error` (required)
  - A human-readable description of the error
  - Type: String

- `code` (required)
  - A machine-readable error code
  - Examples: "INVALID_INPUT", "USER_NOT_FOUND", "CONVERSATION_NOT_FOUND", etc.
  - Type: String

## Authentication
- Requires valid user authentication
- User context is derived from the user_id in the path
- All operations are scoped to the authenticated user

## Authorization
- Users can only access their own conversations
- User ID in path must match authenticated user
- Cross-user data access is prohibited

## Example Requests

### Starting a New Conversation
```
POST /api/user123/chat
Content-Type: application/json

{
  "message": "Add a task to buy milk"
}
```

### Continuing an Existing Conversation
```
POST /api/user123/chat
Content-Type: application/json

{
  "conversation_id": "abc123-def456-ghi789",
  "message": "What's the status of my tasks?"
}
```

## Example Responses

### Successful Response with Tool Call
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "abc123-def456-ghi789",
  "response": "I've added the task 'buy milk' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "buy milk",
        "description": ""
      },
      "result": {
        "success": true,
        "task_id": "task987"
      }
    }
  ]
}
```

### Successful Response without Tool Calls
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "abc123-def456-ghi789",
  "response": "Hello! How can I assist you with your tasks today?",
  "tool_calls": []
}
```