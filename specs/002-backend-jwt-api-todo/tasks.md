---

description: "Task list for JWT-Protected REST API for Todo Application implementation"
---

# Tasks: JWT-Protected REST API for Todo Application

**Input**: Design documents from `/specs/002-backend-jwt-api-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- For this feature: `backend/` directory will be used for the FastAPI application

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure with requirements.txt
- [X] T002 Initialize Python project with FastAPI, SQLModel, PyJWT dependencies
- [ ] T003 [P] Configure linting and formatting tools (ruff, black, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and connection framework in backend/database.py
- [X] T005 [P] Implement JWT authentication framework in backend/auth.py
- [X] T006 [P] Setup API routing structure with proper prefix in backend/main.py
- [X] T007 Create base Task model in backend/models.py
- [X] T008 Configure error handling and logging infrastructure in backend/utils.py
- [X] T009 Setup environment configuration management in backend/config.py
- [X] T010 Implement user data isolation mechanism in backend/security.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Management (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to securely create, read, update, and delete their personal tasks with proper data isolation

**Independent Test**: Authenticate with a JWT token and perform CRUD operations on tasks, ensuring that operations only affect the authenticated user's tasks.

### Implementation for User Story 1

- [X] T011 [P] [US1] Create Task model with user_id relationship in backend/models.py
- [X] T012 [P] [US1] Create TaskCreate and TaskUpdate schemas in backend/schemas.py
- [X] T013 [US1] Implement TaskService in backend/services/task_service.py
- [X] T014 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [X] T015 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [X] T016 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [X] T017 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [X] T018 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [X] T019 [US1] Add validation and error handling for all task operations
- [X] T020 [US1] Add logging for task operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - JWT Authentication Enforcement (Priority: P1)

**Goal**: Ensure all API endpoints require valid JWT authentication and properly enforce user data isolation

**Independent Test**: Make requests to all endpoints both with and without valid JWT tokens, ensuring unauthorized requests are rejected with appropriate HTTP status codes.

### Implementation for User Story 2

- [X] T021 [P] [US2] Enhance JWT verification middleware in backend/auth.py
- [X] T022 [US2] Implement user ID validation middleware to check URL user_id matches token user_id
- [X] T023 [US2] Add 401 Unauthorized responses for missing/invalid JWT tokens
- [X] T024 [US2] Add 403 Forbidden responses for user ID mismatches
- [ ] T025 [US2] Add 404 Not Found responses for non-existent resources
- [ ] T026 [US2] Add 422 Unprocessable Entity responses for validation errors
- [X] T027 [US2] Integrate authentication middleware with all existing endpoints

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion Toggle (Priority: P2)

**Goal**: Allow users to mark tasks as complete or incomplete with a simple operation

**Independent Test**: Create a task, then use the completion toggle endpoint to change its status, verifying the change is persisted correctly.

### Implementation for User Story 3

- [X] T028 [P] [US3] Add PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/routes/tasks.py
- [X] T029 [US3] Implement toggle_completion method in TaskService in backend/services/task_service.py
- [X] T030 [US3] Add validation and error handling for completion toggle operations
- [X] T031 [US3] Add logging for completion toggle operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T032 [P] Documentation updates in backend/docs/
- [X] T033 Code cleanup and refactoring across all modules
- [ ] T034 Performance optimization across all stories
- [ ] T035 [P] Additional unit tests in backend/tests/unit/
- [X] T036 Security hardening of all endpoints
- [X] T037 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model with user_id relationship in backend/models.py"
Task: "Create TaskCreate and TaskUpdate schemas in backend/schemas.py"

# Launch all endpoints for User Story 1 together:
Task: "Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py"
Task: "Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py"
Task: "Implement GET /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
Task: "Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
Task: "Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence