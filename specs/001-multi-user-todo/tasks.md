# Tasks: Multi-User Todo Web Application

**Input**: Design documents from `specs/001-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below DO NOT include test tasks. Manual testing only per specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure (frontend + backend separation)

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend

- [X] T001 [P] Create frontend project structure per Next.js 16+ architecture
- [X] T002 [P] Initialize Next.js 16 project with TypeScript strict mode and Tailwind CSS
- [X] T003 [P] Create backend project structure per FastAPI architecture
- [X] T004 [P] Initialize Python project with FastAPI and dependencies
- [X] T005 [P] Create .env files for frontend and backend (gitignore protected)
- [X] T006 [P] Configure Tailwind CSS 3.4+ for Next.js frontend
- [X] T007 [P] Create shadcn/ui base components (button, input, dialog) for frontend
- [X] T008 [P] Create .gitignore file protecting .env, node_modules, __pycache__

**Checkpoint**: Foundation structure ready - Foundational tasks can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 [P] Create backend database connection and session management
- [X] T010 [P] Configure FastAPI application with CORS middleware
- [X] T011 [P] Create backend dependency injection framework (dependencies.py)
- [X] T012 [P] Create SQLModel User entity in backend/src/models/user.py
- [X] T013 [P] Create SQLModel Task entity in backend/src/models/task.py
- [X] T014 [P] Create Better Auth configuration and JWT token generation in backend/src/auth.py
- [X] T015 [P] Create authentication routes (signup, signin) in backend/src/routers/auth.py
- [X] T016 [P] Create repository pattern for User data access in backend/src/repositories/user_repository.py
- [X] T017 [P] Create repository pattern for Task data access in backend/src/repositories/task_repository.py
- [X] T018 [P] Create service pattern for User business logic in backend/src/services/user_service.py
- [X] T019 [P] Create service pattern for Task business logic in backend/src/services/task_service.py
- [X] T020 [P] Create FastAPI main application entry point in backend/src/main.py

**Checkpoint**: Foundation ready - User story implementation can now begin

---

## Phase 3: User Story 1 - User Account Management (Priority: P1) 🎯 MVP

**Goal**: Users can securely create accounts and sign in to access their personal todo list with JWT authentication

**Independent Test**: Create two separate user accounts and verify both can sign in and receive valid authentication tokens, without any interaction between accounts.

### Tests for User Story 1 (OPTIONAL - manual testing only)

> **NOTE: Manual testing only per specification. No automated test suite for Phase II.**

- [ ] T021 [P] [US1] Manual test: User signup creates account with bcrypt password hash
- [ ] T022 [P] [US1] Manual test: User signin returns valid JWT token with 7-day expiry
- [ ] T023 [P] [US1] Manual test: Duplicate email signup rejected with 409 Conflict
- [ ] T024 [P] [US1] Manual test: Invalid signin credentials return 401 Unauthorized
- [ ] T025 [P] [US1] Manual test: JWT token expires after 7 days and returns 401

### Implementation for User Story 1

- [X] T026 [P] [US1] Implement signup endpoint in backend/src/routers/auth.py using Better Auth
- [X] T027 [P] [US1] Implement signin endpoint in backend/src/routers/auth.py using Better Auth
- [X] T028 [P] [US1] Configure JWT token generation with 7-day expiry (604800 seconds)
- [X] T029 [P] [US1] Add email format validation using standard regex
- [X] T030 [P] [US1] Add email uniqueness check in User service
- [X] T031 [P] [US1] Add password validation (minimum 8 characters) in User service
- [X] T032 [P] [US1] Configure bcrypt password hashing with cost factor 12
- [X] T033 [P] [US1] Create frontend signup page in frontend/app/signup/page.tsx with Next.js 16 async params
- [X] T034 [P] [US1] Create frontend signin page in frontend/app/signin/page.tsx with Next.js 16 async params
- [X] T035 [P] [US1] Create authentication utility in frontend/lib/auth-client.ts for JWT token storage in httpOnly cookies
- [X] T036 [P] [US1] Create API client utility in frontend/lib/api-client.ts for backend communication
- [X] T037 [P] [US1] Add signup form component in frontend/app/components/signup-form.tsx with validation
- [X] T038 [P] [US1] Add signin form component in frontend/app/components/signin-form.tsx with validation
- [X] T039 [P] [US1] Create root layout in frontend/app/layout.tsx with auth context provider
- [X] T040 [P] [US1] Create proxy.ts middleware in frontend/proxy.ts for Next.js 16 request handling and auth checks
- [X] T041 [P] [US1] Configure CORS origins in backend .env and frontend .env.local

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Personal Task Management (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create, view, edit, and delete their own tasks with title (required) and optional description

**Independent Test**: Create multiple tasks, modify them, mark complete/incomplete, and delete them, then verify all changes persist and reflect correctly in user's personal list.

### Tests for User Story 2 (OPTIONAL - manual testing only)

- [ ] T042 [P] [US2] Manual test: Create task with title persists to Neon database
- [ ] T043 [P] [US2] Manual test: List tasks returns user's tasks only (no other users' data)
- [ ] T044 [P] [US2] Manual test: Task update reflects within 200ms
- [ ] T045 [P] [US2] Manual test: Task deletion removes from database after confirmation
- [ ] T046 [P] [US2] Manual test: Toggle completion status updates task and shows visual distinction

### Implementation for User Story 2

- [X] T047 [P] [US2] Create task list page in frontend/app/dashboard/page.tsx with Next.js 16 async params
- [X] T048 [P] [US2] Create task CRUD routes in backend/src/routers/tasks.py (GET list, GET single, POST create, PUT update, DELETE)
- [X] T049 [P] [US2] Implement TaskRepository methods (create, read, update, delete, list_by_user, toggle_complete)
- [X] T050 [P] [US2] Implement TaskService business logic (create_task, get_task, update_task, delete_task, toggle_task)
- [X] T051 [P] [US2] Add ownership verification in TaskService (user_id match)
- [X] T052 [P] [US2] Create task form component in frontend/app/components/task-form.tsx with validation
- [X] T053 [P] [US2] Create task list component in frontend/app/components/task-list.tsx
- [X] T054 [P] [US2] Create task item component in frontend/app/components/task-item.tsx
- [X] T055 [P] [US2] Add task creation API call in frontend/lib/api-client.ts (POST /{user_id}/tasks)
- [X] T056 [P] [US2] Add task list API call in frontend/lib/api-client.ts (GET /{user_id}/tasks)
- [X] T057 [P] [US2] Add single task API call in frontend/lib/api-client.ts (GET /{user_id}/tasks/{task_id})
- [X] T058 [P] [US2] Add task update API call in frontend/lib/api-client.ts (PUT /{user_id}/tasks/{task_id})
- [X] T059 [P] [US2] Add task delete API call in frontend/lib/api-client.ts (DELETE /{user_id}/tasks/{task_id})
- [X] T060 [P] [US2] Add task toggle API call in frontend/lib/api-client.ts (PATCH /{user_id}/tasks/{task_id}/complete)
- [X] T061 [P] [US2] Implement task ordering (created_at DESC, completed at bottom) in list display
- [X] T062 [P] [US2] Add visual distinction for completed tasks (strikethrough + 60% opacity)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Data Isolation and Security (Priority: P1) 🎯 CRITICAL

**Goal**: Complete multi-user data isolation - users cannot see, access, modify, or delete tasks belonging to other users

**Independent Test**: Create two user accounts, each with own tasks, then attempt to access each other's tasks via API and UI to verify complete isolation.

### Tests for User Story 3 (OPTIONAL - manual testing only)

- [X] T063 [P] [US3] Manual test: User A cannot view User B's tasks (returns 404 Not Found)
- [X] T064 [P] [US3] Manual test: User A cannot create task as User B (returns 403 Forbidden, creates for User A)
- [X] T065 [P] [US3] Manual test: User A cannot delete User B's task (returns 404 Not Found)
- [X] T066 [P] [US3] Manual test: Unauthenticated access to protected endpoint returns 401 Unauthorized
- [X] T067 [P] [US3] Manual test: Expired JWT token returns 401 with redirect
- [X] T068 [P] [US3] Manual test: Database foreign key prevents orphaned tasks

### Implementation for User Story 3

**Note**: Security is enforced throughout backend services and frontend client. Key tasks already implement data isolation:

- [X] T069 [P] [US3] Enforce user_id filtering in all TaskRepository queries (list_by_user filters by authenticated user ID)
- [X] T070 [P] [US3] Add ownership verification in all TaskService update/delete methods (returns 404 if user_id mismatch)
- [X] T071 [P] [US3] Configure task routes to verify user_id from URL matches JWT token sub claim
- [X] T072 [P] [US3] Add authentication middleware in FastAPI app (verify JWT on all protected routes)
- [X] T073 [P] [US3] Ensure database foreign key constraint (tasks.user_id → users.id) is enforced by SQLModel
- [X] T074 [P] [US3] Configure CORS to prevent unauthorized cross-origin requests
- [X] T075 [P] [US3] Add JWT token verification in API client (attach to all requests)
- [X] T076 [P] [US3] Create error boundary in frontend for 401/404 responses

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently with complete data isolation

---

## Phase 6: User Story 4 - Responsive User Interface (Priority: P2)

**Goal**: Application works seamlessly on mobile devices (375px width minimum) and desktop screens (1920px width) with modern, intuitive design

**Independent Test**: Access application on mobile viewport (375x667) and desktop viewport (1920x1080), verifying all features work and layout adapts appropriately.

### Tests for User Story 4 (OPTIONAL - manual testing only)

- [X] T077 [P] [US4] Manual test: Mobile viewport (375px) shows all elements with no horizontal scroll
- [X] T078 [P] [US4] Manual test: Desktop viewport (1920px) uses space efficiently
- [X] T079 [P] [US4] Manual test: Loading indicators display during all API operations
- [X] T080 [P] [US4] Manual test: Error messages clear and actionable
- [X] T081 [P] [US4] Manual test: Form validation feedback immediate and specific
- [X] T082 [P] [US4] Manual test: Buttons have minimum touch target size of 44x44 pixels
- [X] T083 [P] [US4] Manual test: Text contrast meets WCAG AA standards (4.5:1 for normal text)

### Implementation for User Story 4

- [X] T084 [P] [US4] Apply Tailwind CSS responsive classes (sm, md, lg, xl breakpoints) to all components
- [X] T085 [P] [US4] Ensure mobile viewport (375px min) has no horizontal scroll
- [X] T086 [P] [US4] Optimize desktop layout for 1920px width with proper margins and spacing
- [X] T087 [P] [US4] Add loading states (spinner) to task form and task list during API calls
- [X] T088 [P] [US4] Add error handling in API client with clear error messages
- [X] T089 [P] [US4] Add form validation feedback (inline error messages) to signup and signin forms
- [X] T090 [P] [US4] Configure Tailwind color palette with WCAG AA contrast ratios
- [X] T091 [P] [US4] Ensure all buttons and interactive elements have minimum touch target size (44x44px)
- [X] T092 [P] [US4] Test responsive behavior on multiple viewport sizes (mobile 375px, tablet 768px, desktop 1920px)

**Checkpoint**: All user stories should now be independently functional with responsive UI

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T093 [P] Documentation updates in README.md with setup instructions
- [X] T094 [P] Code cleanup and refactoring (remove unused imports, improve naming)
- [X] T095 [P] Performance optimization across all stories (verify database queries <100ms, API <200ms)
- [X] T096 [P] Security hardening (verify no secrets in code, all env vars used)
- [X] T097 [P] Run complete user journey test (signup → signin → create task → mark complete → delete task)
- [X] T098 [P] Verify frontend initial load < 2 seconds on standard connection
- [X] T099 [P] Final verification against specification requirements
- [X] T100 [P] Prepare demo presentation for hackathon judges

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: All tasks marked [P] can run in parallel (T001-T008)
- **Foundational Phase**: All tasks marked [P] can run in parallel (T009-T020)
- **User Stories Phase**: Once Foundational phase completes, all 4 user stories can start in parallel (if team capacity allows)
  - US1 tasks: T021-T041 can run in parallel after foundation
  - US2 tasks: T042-T062 can run in parallel after foundation
  - US3 tasks: T063-T076 can run in parallel after foundation
  - US4 tasks: T084-T092 can run in parallel after foundation

### Parallel Example: User Story 1

```bash
# Launch all parallel tasks for US1 (after foundation):
Task: "Implement signup endpoint in backend/src/routers/auth.py"
Task: "Implement signin endpoint in backend/src/routers/auth.py"
Task: "Create frontend signup page in frontend/app/signup/page.tsx"
Task: "Create frontend signin page in frontend/app/signin/page.tsx"
Task: "Create authentication utility in frontend/lib/auth-client.ts"
Task: "Create API client utility in frontend/lib/api-client.ts"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T020)
3. Complete Phase 3: User Story 1 (T021-T041)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Complete Phase 4: User Story 2 (T042-T062)
6. **STOP and VALIDATE**: Test User Story 2 independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo (data isolation)
4. Add User Story 4 → Test independently → Deploy/Demo (responsive UI)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (authentication)
   - Developer B: User Story 2 (task management)
   - Developer C: User Story 3 (data isolation)
   - Developer D: User Story 4 (responsive UI)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are OPTIONAL - manual testing only per specification
- Verify tests fail before implementing (TDD not required for Phase II)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
