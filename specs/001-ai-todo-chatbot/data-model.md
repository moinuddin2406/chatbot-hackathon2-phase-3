# Data Model: AI-Powered Todo Chatbot

## Entity: Conversation

Represents a series of messages between a user and the AI assistant.

### Attributes:
- **id** (UUID, Primary Key)
  - Unique identifier for the conversation
  - Generated automatically when conversation is created
  
- **user_id** (String/UUID, Foreign Key)
  - Reference to the user who owns the conversation
  - Links to the user account in the main application
  
- **created_at** (DateTime)
  - Timestamp when conversation was initiated
  - Automatically set when record is created
  
- **updated_at** (DateTime)
  - Timestamp of last activity in conversation
  - Updated whenever a new message is added

### Relationships:
- One-to-many with Message entity (one conversation, many messages)
- Many-to-one with User entity (many conversations, one user)

## Entity: Message

Represents a single message in a conversation between user and AI.

### Attributes:
- **id** (UUID, Primary Key)
  - Unique identifier for the message
  - Generated automatically when message is created
  
- **conversation_id** (UUID, Foreign Key)
  - Reference to the parent conversation
  - Links to the Conversation entity
  
- **user_id** (String/UUID, Foreign Key)
  - Reference to the user who sent the message
  - Links to the user account in the main application
  
- **role** (String, Enum: "user"|"assistant")
  - Indicates whether the message was sent by the user or AI assistant
  - Required field
  
- **content** (Text)
  - The actual message content
  - Required field
  
- **tool_calls** (JSON, Optional)
  - Optional JSON object containing any tool calls made during this interaction
  - Contains tool name and parameters
  
- **created_at** (DateTime)
  - Timestamp when message was created
  - Automatically set when record is created

### Relationships:
- Many-to-one with Conversation entity (many messages, one conversation)
- Many-to-one with User entity (many messages, one user)

## Entity: Task

Represents a user's task item that can be managed through the chatbot.

### Attributes:
- **id** (UUID, Primary Key)
  - Unique identifier for the task
  - Generated automatically when task is created
  
- **user_id** (String/UUID, Foreign Key)
  - Reference to the user who owns the task
  - Links to the user account in the main application
  
- **title** (String)
  - Brief title of the task
  - Required field
  
- **description** (Text, Optional)
  - Detailed description of the task
  - Optional field for additional context
  
- **completed** (Boolean)
  - Whether the task is completed
  - Default: false
  
- **created_at** (DateTime)
  - Timestamp when task was created
  - Automatically set when record is created
  
- **updated_at** (DateTime)
  - Timestamp of last update to the task
  - Updated whenever the task is modified

### Relationships:
- Many-to-one with User entity (many tasks, one user)

## Validation Rules

### Conversation Validation:
- user_id must exist in the user system
- created_at and updated_at must be valid timestamps
- updated_at must be >= created_at

### Message Validation:
- conversation_id must reference an existing conversation
- user_id must exist in the user system
- role must be either "user" or "assistant"
- content must not be empty
- tool_calls must conform to the defined schema when present
- created_at must be a valid timestamp

### Task Validation:
- user_id must exist in the user system
- title must not be empty
- completed must be a boolean value
- created_at and updated_at must be valid timestamps
- updated_at must be >= created_at

## Indexes

### Conversation Table:
- Index on user_id for efficient user-specific queries
- Index on created_at for chronological sorting
- Composite index on (user_id, created_at) for common query patterns

### Message Table:
- Index on conversation_id for efficient conversation retrieval
- Index on user_id for user-specific queries
- Index on created_at for chronological sorting
- Composite index on (conversation_id, created_at) for conversation history queries

### Task Table:
- Index on user_id for efficient user-specific queries
- Index on completed for filtering by status
- Index on created_at for chronological sorting
- Composite index on (user_id, completed) for common task queries