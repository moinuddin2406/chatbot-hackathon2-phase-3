# Feature Specification: JWT-Protected REST API for Todo Application

**Feature Branch**: `002-jwt-api-todo`
**Created**: 2026-01-09
**Status**: Draft
**Input**: User description: "Scope: Backend Specification Only Phase: Phase II – Todo Full-Stack Web Application Focus: Secure, Stateless, JWT-Protected REST API Integration Target: Next.js Frontend (Better Auth) You are operating under the approved constitution.md. Do NOT modify frontend or database specs unless explicitly required. Do NOT implement code. ──────────────────────────────────── OBJECTIVE ──────────────────────────────────── Define a complete, production-quality backend specification for a multi-user Todo web application that integrates seamlessly with a Next.js frontend using Better Auth and JWT authentication. The backend must: - Be fully stateless - Secure all routes with JWT - Enforce strict user data isolation - Persist data in Neon Serverless PostgreSQL - Integrate cleanly with frontend API client ──────────────────────────────────── TECH STACK (FIXED) ──────────────────────────────────── - Python FastAPI - SQLModel (ORM) - Neon Serverless PostgreSQL - JWT Authentication (issued by Better Auth) - Uvicorn (development server) ──────────────────────────────────── ENVIRONMENT CONFIGURATION ──────────────────────────────────── Backend must read configuration strictly from environment variables: - BETTER_AUTH_SECRET - BETTER_AUTH_URL - DATABASE_URL (Neon PostgreSQL connection string) No secrets may be hardcoded. Failure to read env vars must result in startup error. ──────────────────────────────────── BACKEND RESPONSIBILITIES ──────────────────────────────────── 1. Authentication & Authorization - Verify JWT tokens issued by Better Auth - Validate token signature and expiry - Extract authenticated user identity - Reject unauthenticated requests 2. Task Management API - Create task - List tasks (user-scoped) - Retrieve single task - Update task - Delete task - Toggle completion state 3. Security Enforcement - Every request requires valid JWT - URL user_id must match token user_id - Cross-user access must be blocked - Proper HTTP status codes returned 4. Frontend Integration - Accept Authorization: Bearer <token> header - Return JSON responses only - Provide predictable error responses for frontend handling ──────────────────────────────────── API ENDPOINTS TO SPECIFY ──────────────────────────────────── All routes are prefixed with /api - GET /api/{user_id}/tasks - POST /api/{user_id}/tasks - GET /api/{user_id}/tasks/{id} - PUT /api/{user_id}/tasks/{id} - DELETE /api/{user_id}/tasks/{id} - PATCH /api/{user_id}/tasks/{id}/complete ──────────────────────────────────── API BEHAVIOR REQUIREMENTS ──────────────────────────────────── - Requests without JWT → 401 Unauthorized - Invalid or expired JWT → 401 Unauthorized - user_id mismatch → 403 Forbidden - Resource not found → 404 Not Found - Validation error → 422 Unprocessable Entity All responses must be JSON-serializable. ──────────────────────────────────── DATA ACCESS RULES ──────────────────────────────────── - All database queries must be filtered by authenticated user_id - No endpoint may return or modify another user's data - Task ownership must be enforced at query level - Database access via SQLModel only ──────────────────────────────────── INTEGRATION CONTRACT WITH FRONTEND ──────────────────────────────────── - Backend trusts ONLY the JWT token, not frontend state - Frontend sends JWT via Authorization header - Backend extracts user identity from token - Backend ignores client-provided user identity if mismatched - Error messages must be frontend-consumable ──────────────────────────────────── FILES & STRUCTURE TO SPECIFY ──────────────────────────────────── Specify backend responsibilities for: - main.py (app setup, middleware) - auth.py (JWT verification logic) - routes/tasks.py (task endpoints) - models.py (SQLModel schemas) - db.py (database session & connection) ──────────────────────────────────── QUALITY & NON-FUNCTIONAL REQUIREMENTS ──────────────────────────────────── - Stateless design (no sessions stored server-side) - Clear separation of concerns - Readable and maintainable structure - Predictable API behavior - Production-ready security posture ──────────────────────────────────── CONSTRAINTS ──────────────────────────────────── - Do NOT implement code - Do NOT introduce new endpoints - Do NOT modify frontend behavior - Do NOT bypass JWT validation - Follow constitution.md strictly ──────────────────────────────────── SUCCESS CRITERIA ──────────────────────────────────── Backend specs are complete when: - All endpoints are fully specified - Auth flow is unambiguous - Security rules are explicit - Frontend integration points are clearly defined - A Backend Engineer Agent can implement without questions"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As an authenticated user, I want to securely manage my personal tasks through a REST API that ensures my data is isolated from other users, so that I can organize my work without privacy concerns.

**Why this priority**: This is the core functionality of the application - users need to be able to create, read, update, and delete their tasks securely.

**Independent Test**: Can be fully tested by authenticating with a JWT token and performing CRUD operations on tasks, ensuring that operations only affect the authenticated user's tasks.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** the user creates a new task, **Then** the task is saved to the database and associated with the authenticated user's ID.
2. **Given** a user has multiple tasks in the system, **When** the user requests their task list, **Then** only tasks belonging to the authenticated user are returned.
3. **Given** a user has created tasks, **When** the user updates a specific task, **Then** only that specific task is updated and only if it belongs to the authenticated user.

---

### User Story 2 - JWT Authentication Enforcement (Priority: P1)

As a security-conscious application owner, I want all API endpoints to require valid JWT authentication, so that unauthorized users cannot access or manipulate any data.

**Why this priority**: Security is paramount for a multi-user system. Without proper authentication, the entire application is vulnerable.

**Independent Test**: Can be tested by making requests to all endpoints both with and without valid JWT tokens, ensuring unauthorized requests are rejected with appropriate HTTP status codes.

**Acceptance Scenarios**:

1. **Given** a request to any API endpoint, **When** no JWT token is provided in the Authorization header, **Then** the system returns a 401 Unauthorized response.
2. **Given** a request to any API endpoint, **When** an invalid or expired JWT token is provided, **Then** the system returns a 401 Unauthorized response.
3. **Given** a request to an API endpoint with a valid JWT token, **When** the user ID in the URL doesn't match the user ID in the token, **Then** the system returns a 403 Forbidden response.

---

### User Story 3 - Task Completion Toggle (Priority: P2)

As a user managing my tasks, I want to be able to mark tasks as complete or incomplete with a simple operation, so that I can track my progress efficiently.

**Why this priority**: This is a common and important interaction in task management applications that enhances user productivity.

**Independent Test**: Can be tested by creating a task, then using the completion toggle endpoint to change its status, verifying the change is persisted correctly.

**Acceptance Scenarios**:

1. **Given** a user has an incomplete task, **When** the user toggles the completion status, **Then** the task's completion status is updated to complete.
2. **Given** a user has a completed task, **When** the user toggles the completion status again, **Then** the task's completion status is updated back to incomplete.

---

### Edge Cases

- What happens when a JWT token expires mid-request?
- How does the system handle requests with malformed JWT tokens?
- What occurs when a user attempts to access a task that doesn't exist?
- How does the system respond when database connection fails during an operation?
- What happens when a user tries to access another user's tasks with a valid token?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens issued by Better Auth before processing any request
- **FR-002**: System MUST validate token signature and expiry before allowing access to resources
- **FR-003**: System MUST extract authenticated user identity from the JWT token
- **FR-004**: System MUST reject all unauthenticated requests with HTTP 401 status
- **FR-005**: System MUST allow users to create new tasks via POST /api/{user_id}/tasks
- **FR-006**: System MUST allow users to retrieve their task list via GET /api/{user_id}/tasks
- **FR-007**: System MUST allow users to retrieve a specific task via GET /api/{user_id}/tasks/{id}
- **FR-008**: System MUST allow users to update a specific task via PUT /api/{user_id}/tasks/{id}
- **FR-009**: System MUST allow users to delete a specific task via DELETE /api/{user_id}/tasks/{id}
- **FR-010**: System MUST allow users to toggle task completion via PATCH /api/{user_id}/tasks/{id}/complete
- **FR-011**: System MUST ensure URL user_id matches the token's user_id, returning HTTP 403 if they don't match
- **FR-012**: System MUST return HTTP 404 when requested resources are not found
- **FR-013**: System MUST return HTTP 422 for validation errors in request data
- **FR-014**: System MUST filter all database queries by authenticated user_id to enforce data isolation
- **FR-015**: System MUST accept Authorization header with Bearer token format
- **FR-016**: System MUST return only JSON-serializable responses
- **FR-017**: System MUST read configuration from environment variables (BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL)
- **FR-018**: System MUST fail to start if required environment variables are missing

### Key Entities

- **Task**: Represents a user's task with properties like title, description, completion status, and creation date. Each task is owned by a specific user.
- **User**: Represents an authenticated user in the system, identified by a unique user ID extracted from the JWT token.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can authenticate with JWT tokens and perform all task operations with 99.9% success rate
- **SC-002**: System processes authenticated requests with an average response time under 200ms
- **SC-003**: 100% of unauthorized requests are properly rejected with appropriate HTTP status codes
- **SC-004**: Users can only access their own tasks, with 0% cross-user data access incidents
- **SC-005**: API endpoints return consistent JSON responses that can be consumed by the Next.js frontend
- **SC-006**: System successfully reads all required environment variables at startup without errors
- **SC-007**: Backend API can handle 1000+ concurrent authenticated users without degradation
