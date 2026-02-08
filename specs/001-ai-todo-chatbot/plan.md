# Implementation Plan: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-todo-chatbot
**Created**: 2026-02-06
**Status**: Draft

## Technical Context

This implementation plan details the construction of an AI-powered Todo Chatbot that integrates into an existing full-stack application. The system will use Cohere API as the language model, FastAPI for the backend, MCP server for task operations, and maintain database-persisted, stateless conversations. The frontend will feature a chatbot UI with an icon-triggered chat panel.

**Technologies**:
- Backend: FastAPI
- AI Model: Cohere API
- Agent Pattern: OpenAI Agents SDK-style (Agent, Runner, Tool calls)
- Tool Layer: MCP server
- Frontend: Web UI with chatbot icon
- Database: SQL-based with conversation persistence

**Architecture Overview**:
- Frontend: Chatbot UI with floating icon and collapsible chat panel
- Backend: Stateless chat endpoint with conversation persistence
- AI Layer: Cohere-based agent with intent detection and tool routing
- MCP Server: Tool server exposing task operations
- Database: Stores tasks, conversations, and messages

## Constitution Check

This implementation must comply with the project constitution:

- ✅ **SINGLE SOURCE OF TRUTH**: Database will be the only source of truth for tasks, conversations, and messages
- ✅ **STATELESS ARCHITECTURE**: Each chat request will be independent with conversation context reconstructed from database
- ✅ **TOOL-FIRST INTELLIGENCE**: All task operations will happen through MCP tools, not directly from AI
- ✅ **COHERE AS PRIMARY LLM**: Only Cohere API will be used for language understanding and generation
- ✅ **Security & Auth**: Each request will be scoped to user_id with proper data isolation

## Gates

- [ ] All architectural decisions align with constitution
- [ ] Technology stack matches requirements
- [ ] Data flow respects stateless design
- [ ] Security measures prevent cross-user data access
- [ ] Error handling follows constitutional guidelines

---

## Phase 0: Outline & Research

### Research Findings

#### 1. Cohere API Integration Patterns
**Decision**: Use Cohere's chat completions endpoint with tool calling capabilities
**Rationale**: Cohere's tool calling feature allows us to define functions that the model can call, which fits perfectly with our MCP tool server approach
**Alternatives considered**: Using generative completions with custom parsing, but tool calling provides more reliable intent detection

#### 2. FastAPI-MCP Integration Approach
**Decision**: Implement MCP server as a separate service that communicates with the main FastAPI backend via HTTP or IPC
**Rationale**: Maintains clear separation of concerns while allowing flexible deployment options
**Alternatives considered**: Direct function imports vs. service-to-service communication

#### 3. Frontend Chat UI Component Strategy
**Decision**: Create a React-based floating chat widget that can be integrated into existing pages
**Rationale**: Allows easy integration with the existing Next.js frontend without major refactoring
**Alternatives considered**: Standalone chat page vs. embedded widget

#### 4. Conversation Reconstruction Efficiency
**Decision**: Implement efficient database queries with pagination for long conversations
**Rationale**: Ensures performance even with lengthy conversation histories
**Alternatives considered**: Caching vs. direct database queries

---

## Phase 1: Design & Contracts

### Data Model

#### Conversation Entity
- `id` (UUID): Unique identifier for the conversation
- `user_id` (String/UUID): Reference to the user who owns the conversation
- `created_at` (DateTime): Timestamp when conversation was initiated
- `updated_at` (DateTime): Timestamp of last activity in conversation

#### Message Entity
- `id` (UUID): Unique identifier for the message
- `conversation_id` (UUID): Reference to the parent conversation
- `user_id` (String/UUID): Reference to the user who sent the message
- `role` (String): Either "user" or "assistant"
- `content` (Text): The actual message content
- `tool_calls` (JSON): Optional tool calls made during this interaction
- `created_at` (DateTime): Timestamp when message was created

#### Task Entity
- `id` (UUID): Unique identifier for the task
- `user_id` (String/UUID): Reference to the user who owns the task
- `title` (String): Brief title of the task
- `description` (Text): Detailed description of the task
- `completed` (Boolean): Whether the task is completed
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp of last update

### API Contracts

#### Chat Endpoint
```
POST /api/{user_id}/chat
```

**Request Body**:
```json
{
  "conversation_id": "string (optional)",
  "message": "string (required)"
}
```

**Response**:
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": "array (optional)"
}
```

**Behavior**:
- If conversation_id is missing, create a new conversation
- Fetch previous messages from DB for context
- Append new user message
- Process through AI agent
- Store messages in DB
- Return AI response

#### MCP Tool Contracts
```
POST /mcp/add_task
```
```json
{
  "user_id": "string",
  "title": "string",
  "description": "string"
}
```

```
POST /mcp/list_tasks
```
```json
{
  "user_id": "string",
  "status": "string (optional: all, pending, completed)"
}
```

```
POST /mcp/complete_task
```
```json
{
  "user_id": "string",
  "task_id": "string"
}
```

```
POST /mcp/update_task
```
```json
{
  "user_id": "string",
  "task_id": "string",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

```
POST /mcp/delete_task
```
```json
{
  "user_id": "string",
  "task_id": "string"
}
```

### Quickstart Guide

1. **Setup Backend Services**:
   - Install dependencies for FastAPI backend
   - Configure database connection
   - Set up Cohere API key
   - Start MCP tool server

2. **Configure Frontend**:
   - Integrate chatbot UI component
   - Configure API endpoints
   - Set up authentication context

3. **Run the Application**:
   - Start backend services
   - Start frontend development server
   - Access the chatbot via the floating icon

### System Architecture Breakdown

#### Frontend Components
- **Floating Chat Icon**: Visible on all pages, triggers chat panel
- **Chat Panel**: Collapsible UI with message history and input
- **Message Display**: Renders messages in chat bubble format
- **Loading Indicators**: Shows processing state during AI responses
- **Error Handlers**: Displays user-friendly error messages

#### Backend API Layers
- **Authentication Middleware**: Verifies user identity and scopes requests
- **Chat Endpoint**: Orchestrates the conversation flow
- **AI Agent Service**: Processes user input and manages tool calls
- **Message Persistence**: Handles storing and retrieving conversation history
- **MCP Client**: Communicates with the MCP tool server

#### AI Agent Layer
- **Cohere Client**: Interfaces with Cohere API
- **Intent Detection**: Determines user intent from natural language
- **Tool Router**: Maps intents to appropriate MCP tools
- **Response Generator**: Creates user-friendly responses based on tool results

#### MCP Tool Server
- **Tool Registry**: Maintains available tools and their schemas
- **Task Operations**: Implements add, list, update, complete, delete functions
- **Database Interface**: Handles all data persistence for tasks
- **Validation Layer**: Ensures data integrity and user access controls

#### Database Layer
- **Conversation Table**: Stores conversation metadata
- **Message Table**: Stores individual messages with context
- **Task Table**: Stores user tasks with status
- **User Association**: Links all data to appropriate users

### Data Flow Between Components

1. **Request Initiation**:
   - User interacts with frontend chat UI
   - Frontend sends message to backend API endpoint
   - Authentication middleware validates user identity

2. **Conversation Reconstruction**:
   - Backend retrieves conversation history from database
   - Previous messages are assembled in chronological order
   - Context is prepared for AI processing

3. **AI Processing**:
   - AI agent receives user message and conversation history
   - Cohere API processes input and determines intent
   - Tool calls are identified and prepared

4. **Tool Execution**:
   - AI agent calls appropriate MCP tools
   - MCP server executes requested operations
   - Results are returned to AI agent

5. **Response Generation**:
   - AI agent generates user-friendly response based on tool results
   - Response is sent back to frontend
   - Both user message and AI response are stored in database

6. **Frontend Update**:
   - Frontend receives AI response
   - Message is displayed in chat interface
   - UI updates to reflect any changes in task state

### Backend Implementation Plan

#### Step 1: Project Structure Setup
- Create new directories for chatbot components
- Set up FastAPI application structure
- Configure logging and error handling

#### Step 2: Configuration Management
- Define environment variables for API keys and endpoints
- Set up configuration loading mechanism
- Implement secret management approach

#### Step 3: Database Models & Migrations
- Define SQLAlchemy/SQLModel models for Conversation, Message, and Task
- Create Alembic migration scripts
- Implement database session management

#### Step 4: Chat API Endpoint Creation
- Implement the POST /api/{user_id}/chat endpoint
- Add request/response validation
- Connect to authentication system

#### Step 5: Conversation Persistence Logic
- Implement functions to load/save conversation history
- Create message serialization/deserialization
- Add pagination for long conversations

#### Step 6: Error Handling & Validation
- Add comprehensive input validation
- Implement error response formatting
- Create custom exception handlers

### AI Agent & Cohere Integration Plan

#### Step 1: Cohere Client Initialization
- Set up Cohere API client with proper authentication
- Implement retry logic for API calls
- Add rate limiting to respect API limits

#### Step 2: Prompt Structure Definition
- Create system prompt defining agent behavior
- Define conversation context formatting
- Establish tool schema definitions

#### Step 3: Tool Schema Exposure
- Define JSON schemas for each MCP tool
- Register tools with Cohere API
- Ensure schemas match actual tool signatures

#### Step 4: Intent Detection & Tool Routing
- Implement logic to extract tool calls from AI response
- Map tool calls to actual MCP endpoints
- Handle parameter validation before forwarding

#### Step 5: Result Injection & Response Generation
- Capture results from MCP tool calls
- Inject results back into conversation context
- Generate final user-friendly response

#### Step 6: Stateless Design Implementation
- Ensure no session state is maintained between requests
- Reconstruct full context from database each time
- Verify all necessary information is persisted

### MCP Tool Server Plan

#### Step 1: Server Initialization
- Set up FastAPI application for MCP server
- Define standard tool server interface
- Implement health check endpoints

#### Step 2: Tool Registration System
- Create registry for available tools
- Define standard tool signature format
- Implement dynamic tool loading

#### Step 3: Input Validation Strategy
- Validate all incoming tool parameters
- Implement type checking and sanitization
- Add user permission verification

#### Step 4: Output Schema Consistency
- Define standard response format for all tools
- Ensure consistent error reporting
- Implement result serialization

#### Step 5: Error Propagation Rules
- Map internal errors to user-friendly messages
- Log errors appropriately without exposing details
- Implement graceful degradation for partial failures

#### MCP AI-Agnostic Design
- Keep tool implementations separate from AI logic
- Use generic data structures that any AI system can consume
- Maintain clear input/output contracts

### Frontend Chatbot UI Plan

#### Step 1: Chat Icon Implementation
- Create floating icon component
- Implement positioning that works across pages
- Add smooth animation for visibility toggling

#### Step 2: Chat Panel Layout
- Design collapsible panel with message history
- Create input area with send button
- Implement responsive design for all screen sizes

#### Step 3: Message Rendering Lifecycle
- Create components for user and AI messages
- Implement proper message formatting
- Add support for tool call visualization if needed

#### Step 4: Loading & Error States
- Design loading indicators for AI processing
- Create error message display components
- Implement retry functionality where appropriate

#### Step 5: API Integration Flow
- Connect UI components to backend API
- Implement proper authentication headers
- Handle connection failures gracefully

#### Step 6: UX Flow Implementation
- Design the complete flow from icon click to response
- Implement auto-scrolling to latest message
- Add keyboard shortcuts for better UX

### Database & State Management Plan

#### Step 1: Table Relationship Design
- Define foreign key relationships between entities
- Create indexes for efficient querying
- Plan partitioning strategy if needed

#### Step 2: Conversation Reconstruction Logic
- Implement efficient query to fetch conversation history
- Add caching layer if needed for performance
- Handle large conversation histories with pagination

#### Step 3: Message Ordering Strategy
- Ensure messages are retrieved in chronological order
- Implement proper timezone handling
- Add support for message threading if needed

#### Step 4: User Isolation Strategy
- Implement row-level security for data isolation
- Add user_id checks to all queries
- Verify no cross-user data access is possible

#### Stateless Request Context Rebuilding
- Create utility functions to reconstruct conversation state
- Implement efficient data loading patterns
- Add error handling for missing conversation data

### Security & Scalability Plan

#### Step 1: User Scoping Implementation
- Verify user_id is validated in all requests
- Implement proper authentication checks
- Add audit logging for sensitive operations

#### Step 2: Input Sanitization
- Sanitize all user inputs before processing
- Implement protection against injection attacks
- Validate all data before database insertion

#### Step 3: Rate Limiting
- Implement rate limiting for API endpoints
- Add protection against abuse patterns
- Monitor and alert on unusual usage patterns

#### Step 4: Horizontal Scaling Preparation
- Design stateless services that can scale horizontally
- Implement proper load balancing
- Prepare for distributed caching if needed

### Testing & Validation Plan

#### Step 1: Unit Testing Targets
- Test individual components in isolation
- Mock external dependencies like Cohere API
- Validate data models and validation logic

#### Step 2: Integration Testing Flow
- Test the complete flow from UI to database
- Validate conversation persistence across requests
- Test error handling scenarios

#### Step 3: AI Behavior Validation
- Create test cases for different user inputs
- Validate tool call accuracy
- Test edge cases and error conditions

#### Step 4: Tool-Call Correctness Checks
- Verify all MCP tools are called with correct parameters
- Test tool chaining scenarios
- Validate error propagation from tools

### Deployment & Environment Plan

#### Step 1: Backend Deployment Flow
- Containerize backend services using Docker
- Set up CI/CD pipeline for deployments
- Configure environment-specific settings

#### Step 2: Frontend Deployment Flow
- Build static assets for production
- Deploy to CDN or hosting service
- Implement proper caching strategies

#### Step 3: Environment Variable Handling
- Securely manage API keys and secrets
- Implement environment-specific configurations
- Set up configuration validation

#### Step 4: API Base URL Configuration
- Configure backend API endpoints for frontend
- Set up CORS policies appropriately
- Implement environment-specific URL routing

### Risks & Mitigation

#### Risk 1: AI Misinterpretation
- **Risk**: AI incorrectly interprets user intent leading to wrong actions
- **Mitigation**: Implement confidence scoring and user confirmation for destructive actions

#### Risk 2: Tool Failure
- **Risk**: MCP tools fail unexpectedly causing poor user experience
- **Mitigation**: Implement retry logic and graceful degradation with clear error messages

#### Risk 3: UI Latency Issues
- **Risk**: Slow responses from AI or backend affecting user experience
- **Mitigation**: Implement loading states and optimistic UI updates where appropriate

#### Risk 4: Deployment Mismatch
- **Risk**: Different environments having inconsistent configurations
- **Mitigation**: Implement configuration validation and environment parity practices

---

## Phase 2: Implementation Steps (High-Level)

1. **Setup Infrastructure**
   - Initialize database schema
   - Set up Cohere API integration
   - Configure MCP tool server

2. **Build Core Backend**
   - Implement chat API endpoint
   - Create conversation persistence layer
   - Develop AI agent service

3. **Develop MCP Tools**
   - Implement task CRUD operations
   - Add user validation and security
   - Create tool schemas for AI

4. **Create Frontend UI**
   - Build floating chat component
   - Implement message display
   - Add loading/error states

5. **Integration & Testing**
   - Connect all components
   - Perform end-to-end testing
   - Validate security measures

6. **Deployment Preparation**
   - Create deployment configurations
   - Set up monitoring and logging
   - Prepare documentation

This implementation plan aligns with the approved specification and follows the project constitution. All components are designed to work together while maintaining the required stateless architecture and security measures.