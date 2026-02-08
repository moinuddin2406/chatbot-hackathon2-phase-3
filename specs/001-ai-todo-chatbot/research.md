# Research Findings: AI-Powered Todo Chatbot

## 1. Cohere API Integration Patterns

**Decision**: Use Cohere's chat completions endpoint with tool calling capabilities
**Rationale**: Cohere's tool calling feature allows us to define functions that the model can call, which fits perfectly with our MCP tool server approach. This enables reliable intent detection and structured tool usage.
**Alternatives considered**: 
- Using generative completions with custom parsing (would be less reliable for intent detection)
- Using other LLM providers (would violate the requirement to use Cohere exclusively)

## 2. FastAPI-MCP Integration Approach

**Decision**: Implement MCP server as a separate service that communicates with the main FastAPI backend via HTTP
**Rationale**: Maintains clear separation of concerns while allowing flexible deployment options. This approach keeps the AI agent layer cleanly separated from the data manipulation layer.
**Alternatives considered**: 
- Direct function imports (would create tight coupling between services)
- Shared database access without API layer (would bypass the MCP tool server requirement)

## 3. Frontend Chat UI Component Strategy

**Decision**: Create a React-based floating chat widget that can be integrated into existing pages
**Rationale**: Allows easy integration with the existing Next.js frontend without major refactoring. The floating widget approach provides a consistent user experience across all pages.
**Alternatives considered**: 
- Standalone chat page (would require users to navigate away from their current context)
- Embedded chat in specific sections only (would limit accessibility)

## 4. Conversation Reconstruction Efficiency

**Decision**: Implement efficient database queries with pagination for long conversations, with a reasonable limit on how many messages to load at once
**Rationale**: Ensures performance even with lengthy conversation histories while maintaining context for the AI model. A sliding window approach will keep recent context while not overwhelming the system.
**Alternatives considered**: 
- Loading entire conversation history (could become slow with long conversations)
- Caching conversation state in memory (would violate the stateless architecture requirement)

## 5. Database Technology Selection

**Decision**: Use the existing database technology (likely PostgreSQL based on project structure) to maintain consistency with the existing application
**Rationale**: Leverages existing infrastructure and knowledge rather than introducing a new database technology. Maintains consistency with the existing backend architecture.
**Alternatives considered**: 
- Using a different database technology (would increase complexity and maintenance overhead)

## 6. Authentication and User Scoping

**Decision**: Leverage the existing authentication system in the application and pass user context through the API calls
**Rationale**: Integrates cleanly with the existing security architecture without duplicating authentication logic. Ensures user data isolation as required.
**Alternatives considered**: 
- Implementing a separate authentication system (would create security inconsistencies)
- Passing user tokens directly to the AI layer (would violate the principle of keeping AI layer stateless)