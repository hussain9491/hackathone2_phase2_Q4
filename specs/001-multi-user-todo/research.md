# Research: Multi-User Todo Web Application

**Date**: 2026-01-06
**Feature**: [spec.md](spec.md)
**Status**: Complete

## Research Topics

All technical decisions clarified from specification. No NEEDS CLARIFICATION markers in spec - all requirements are clear and aligned with constitution-mandated technology stack.

### 1. Next.js 16 Breaking Changes

**Decision**: Use Next.js 16 with App Router and async params/searchParams
**Rationale**: Constitution mandates Next.js 16+. Next.js 16 introduces breaking changes that must be handled correctly to avoid runtime errors.
**Alternatives considered**:
- Next.js 15: Rejected - Constitution mandates Next.js 16+
**Key patterns required**:
- `params` and `searchParams` are now Promises, must use `await`
- Client components need `use()` hook for Promises
- Middleware renamed to `proxy.ts`

**Implementation reference**: [building-nextjs-apps](../../../.claude/skills/building-nextjs-apps/SKILL.md)

### 2. Better Auth with JWT Plugin

**Decision**: Use Better Auth with JWT plugin for authentication
**Rationale**: Constitution mandates Better Auth. JWT plugin provides stateless authentication with 7-day token expiry. Better Auth handles password hashing (bcrypt) and session management.
**Alternatives considered**:
- Manual JWT implementation: Rejected - Violates spec-driven principle, Better Auth provides battle-tested solution
- OAuth (Google, GitHub): Rejected - Out of scope per spec
**Key configuration required**:
- BETTER_AUTH_SECRET: Minimum 32 characters, identical in frontend and backend
- Session expiresIn: 7 days (604800 seconds)
- Password hashing: bcrypt with cost factor 12
- PKCE enabled for security

**Implementation reference**: [configuring-better-auth](../../../.claude/skills/configuring-better-auth/SKILL.md)

### 3. SQLModel with Async PostgreSQL

**Decision**: Use SQLModel ORM with async/await patterns
**Rationale**: Constitution mandates SQLModel 0.0.14+. SQLModel provides type-safe database access, prevents SQL injection, and includes Pydantic for validation. Async patterns required for performance (<200ms constraint).
**Alternatives considered**:
- SQLAlchemy direct: Rejected - Less type safety, more boilerplate
- Drizzle ORM: Rejected - Constitution mandates SQLModel
**Key patterns required**:
- AsyncSession for all database operations
- Async engine with `postgresql+asyncpg://` connection string
- Foreign key relationships enforced via SQLModel Field
- Timestamps (created_at, updated_at) on all records
- Cascade deletion for user → tasks relationship

**Implementation reference**: [scaffolding-fastapi-dapr](../../../.claude/skills/scaffolding-fastapi-dapr/SKILL.md)

### 4. FastAPI Backend Architecture

**Decision**: Use FastAPI with repository + service pattern
**Rationale**: FastAPI provides async support, automatic OpenAPI docs, and high performance. Repository + service pattern separates data access from business logic, improving testability and maintainability.
**Alternatives considered**:
- Flask: Rejected - No native async support, slower
- Django: Rejected - Constitution mandates FastAPI
**Key patterns required**:
- Dependency injection via FastAPI Depends
- Async route handlers
- HTTPException for error handling
- CORS middleware configuration
- OpenAPI/Swagger auto-documentation

**Implementation reference**: [scaffolding-fastapi-dapr](../../../.claude/skills/scaffolding-fastapi-dapr/SKILL.md)

### 5. User Data Isolation Strategy

**Decision**: Multi-tenant isolation at database query level with API ownership verification
**Rationale**: Constitution requires strict user isolation. Database-level filtering prevents cross-user data leakage. API-level ownership verification provides defense-in-depth.
**Alternatives considered**:
- Schema per user: Rejected - Overly complex for demo, Neon connection single database
- Row-level security (RLS): Rejected - SQLModel doesn't support natively
**Key patterns required**:
- All task queries filter by `user_id` from JWT token
- Ownership verification on update/delete operations
- Return 404 Not Found (not 401) for ownership violations (security best practice)
- Foreign key constraint: `tasks.user_id → users.id`

### 6. Responsive UI with Tailwind CSS

**Decision**: Use Tailwind CSS 3.4+ with mobile-first approach
**Rationale**: Constitution mandates Tailwind CSS 3.4+. Mobile-first design ensures responsiveness across viewport sizes (375px to 1920px). Tailwind provides utility classes for rapid development.
**Alternatives considered**:
- CSS-in-JS (styled-components): Rejected - More complexity, Tailwind mandated
- Shadcn/ui components: Selected - Leverages Tailwind, provides pre-built accessible components
**Key patterns required**:
- Mobile viewport: 375px minimum, no horizontal scroll
- Desktop viewport: 1920px optimized
- Tailwind responsive classes (sm, md, lg, xl breakpoints)
- Shadcn/ui components for consistency
- WCAG AA contrast ratios (4.5:1 for normal text)
- Touch target size 44x44 pixels minimum

**Implementation reference**: [styling-with-shadcn](../../../.claude/skills/styling-with-shadcn/SKILL.md)

### 7. API Design and Error Handling

**Decision**: RESTful API with consistent error format and standard HTTP status codes
**Rationale**: Constitution mandates `/api/` prefix, user_id in URL path, and standard status codes. Consistency enables predictable client handling.
**Key patterns required**:
- All endpoints: `/api/{user_id}/tasks` and `/api/{user_id}/tasks/{task_id}`
- Status codes: 200, 201, 400, 401, 403, 404, 409, 500
- Consistent error response: `{ "error": "message" }`
- Authentication: JWT in `Authorization: Bearer <token>` header
- CORS: Frontend origin whitelisted

### 8. Performance Optimization

**Decision**: Database indexes, query optimization, no N+1 problems
**Rationale**: Constitution mandates <200ms API response and <100ms database query for 100 tasks. Performance is critical success criterion.
**Key strategies**:
- Index on `tasks.user_id` for fast filtering
- Index on `tasks.created_at` for ordering
- Single query to fetch user's tasks (no separate count query)
- Async database operations throughout
- Frontend code splitting and lazy loading for <2s initial load

### 9. Environment Variables and Secrets Management

**Decision**: All secrets in environment variables, .gitignore protects .env
**Rationale**: Constitution prohibits hardcoded secrets. Environment variables enable configuration across environments without code changes.
**Key requirements**:
- Backend .env: DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS
- Frontend .env.local: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- .env and .env.local in .gitignore
- .env.example committed with placeholders

### 10. Database Schema and Relationships

**Decision**: Two-table schema (users, tasks) with foreign key and timestamps
**Rationale**: Constitution mandates PostgreSQL storage with foreign key constraints. Simple schema meets requirements while maintaining data integrity.
**Schema decisions**:
- Users table: id, email, password_hash, created_at, updated_at
- Tasks table: id, user_id (FK → users.id), title, description, completed, created_at, updated_at
- Cascade deletion: user delete removes all tasks
- Unique constraint: users.email
- Indexes: tasks.user_id, tasks.created_at

## Unresolved Questions

None. All technical decisions made based on constitution requirements and specification constraints.

## References

- [Building Next.js Apps Skill](../../../.claude/skills/building-nextjs-apps/SKILL.md)
- [Configuring Better Auth Skill](../../../.claude/skills/configuring-better-auth/SKILL.md)
- [Scaffolding FastAPI with Dapr Skill](../../../.claude/skills/scaffolding-fastapi-dapr/SKILL.md)
- [Styling with Shadcn Skill](../../../.claude/skills/styling-with-shadcn/SKILL.md)
- [Project Constitution](../../../.specify/memory/constitution.md)
- [Feature Specification](spec.md)
