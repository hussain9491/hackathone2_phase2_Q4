<!--
Sync Impact Report
===================
Version Change: [none] → 1.0.0
Modified Principles: None (initial version)
Added Sections:
  - Core Principles (4 principles)
  - Key Standards (4 standard categories)
  - Constraints (4 constraint categories)
  - Success Criteria (4 criteria categories)
  - Non-Negotiable Rules
Removed Sections: None
Templates Requiring Updates: ✅ All reviewed - no updates needed
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. User-Centric Security
Every user's data is isolated and protected. Authentication required for all operations. No user can access another user's tasks.

**Rationale**: Multi-user systems demand strict data isolation. Without authentication and scoped queries, users can accidentally or maliciously access each other's data, violating privacy and integrity.

### II. Spec-Driven Development
No manual coding allowed. All implementation via Claude Code following specifications. Changes documented in specs before implementation.

**Rationale**: Ensures traceability, prevents undocumented changes, and maintains architectural integrity. Human review at checkpoints prevents drift from approved specifications.

### III. API-First Architecture
RESTful API design standards. Clear separation between frontend and backend. Stateless authentication via JWT.

**Rationale**: Enables independent evolution of frontend/backend, simplifies testing, and supports multiple clients (web, mobile) sharing the same API contract.

### IV. Data Integrity
Persistent storage in PostgreSQL. Transactional operations. Foreign key constraints enforced.

**Rationale**: PostgreSQL provides ACID guarantees ensuring data consistency. Foreign keys enforce referential integrity preventing orphaned records.

## Key Standards

### Code Quality
TypeScript strict mode for frontend. Python type hints for backend. No hardcoded credentials. Environment variables for all secrets.

**Rationale**: Type safety prevents runtime errors. Environment variables enable configuration across environments without code changes.

### Security Standards
JWT tokens expire after 7 days. Passwords hashed using industry-standard algorithms. HTTPS required in production. CORS properly configured.

**Rationale**: Token expiration limits exposure windows. Proper hashing prevents credential leakage. HTTPS protects data in transit. CORS controls cross-origin access.

### API Conventions
All endpoints prefixed with `/api/`. User ID in URL path for resource scoping. Standard HTTP status codes (200, 201, 401, 404, 500). Consistent error response format.

**Rationale**: Consistent prefix prevents collision with frontend routes. URL path scoping enables routing logic. Standard status codes enable predictable client handling.

### Database Standards
Use SQLModel ORM for all database operations. Foreign key relationships properly defined. Timestamps on all records (created_at, updated_at). Soft deletes preferred over hard deletes.

**Rationale**: ORM abstraction prevents SQL injection and provides type safety. Foreign keys enforce referential integrity. Timestamps enable auditing. Soft deletes preserve data for recovery.

## Constraints

### Technology Stack (Non-Negotiable)
Frontend: Next.js 16+ with App Router. Backend: Python FastAPI. Database: Neon Serverless PostgreSQL. ORM: SQLModel. Authentication: Better Auth with JWT.

**Rationale**: Selected stack balances productivity, performance, and developer experience. Neon provides serverless PostgreSQL with built-in scaling. Better Auth handles auth complexity.

### Development Process
Workflow: Write spec → Generate plan → Break into tasks → Implement. All implementation through Claude Code. Human review at defined checkpoints. No deviations from approved specifications.

**Rationale**: Structured workflow ensures completeness and traceability. Human review at checkpoints catches issues early. No deviations prevent scope creep and architectural drift.

### Performance Requirements
API response time < 200ms for CRUD operations. Frontend initial load < 2 seconds. Database queries optimized with proper indexes.

**Rationale**: 200ms target provides responsive user experience. 2-second initial load meets user expectations. Indexes prevent full table scans at scale.

### Data Limits
Task title: 1-200 characters. Task description: max 1000 characters. Maximum 1000 tasks per user (soft limit).

**Rationale**: Character limits enforce conciseness and prevent abuse. 1000 task limit provides reasonable boundary while preventing resource exhaustion.

## Success Criteria

### Functional Requirements Met
All 5 basic CRUD operations working. User authentication (signup/signin) functional. Multi-user isolation verified. Data persists across sessions.

**Rationale**: Completeness of core functionality defines readiness. Isolation verification validates security posture. Persistence confirms data integrity.

### Security Validated
JWT tokens properly signed and verified. Users cannot access other users' data. All endpoints require authentication. Passwords never stored in plain text.

**Rationale**: Proper token validation prevents forged authentication. Isolation testing confirms tenant separation. Endpoint coverage ensures no bypass paths. Hashing prevents credential exposure.

### Code Quality Achieved
No manual coding violations. All specs followed precisely. Type safety enforced. Environment variables used for secrets.

**Rationale**: Manual coding violations indicate workflow bypass. Spec adherence ensures design intent realized. Type safety prevents runtime errors. Env variables prevent credential leakage.

### Documentation Complete
All spec files created and approved. API endpoints documented. Setup instructions clear. Architecture diagrams included.

**Rationale**: Documentation enables onboarding and maintenance. Setup instructions reduce friction. Architecture diagrams communicate design decisions.

## Non-Negotiable Rules

1. **Authentication Required**: Every API endpoint (except signup/signin) MUST verify JWT token. No exceptions.
2. **User Isolation**: All database queries MUST filter by authenticated user ID. No global queries without explicit justification.
3. **No Manual Coding**: All code changes MUST originate from specs → plan → tasks workflow. Direct file edits prohibited.
4. **Type Safety**: TypeScript strict mode and Python type hints MUST be enforced. No `any` or untyped code.
5. **Environment Variables**: All secrets and configuration MUST use environment variables. No hardcoded values.
6. **HTTP Standards**: API endpoints MUST use appropriate status codes. No 200 for errors, no 500 for validation failures.
7. **Timestamps**: All database records MUST include created_at and updated_at. No exceptions.
8. **Foreign Keys**: All relationships MUST use foreign key constraints. No manual relationship enforcement.
9. **CORS Configuration**: CORS MUST be properly configured. No wildcard (*) origins in production.
10. **Password Hashing**: Passwords MUST use industry-standard hashing algorithm (bcrypt or Argon2). No plain text or weak hashes.

## Governance

Constitution supersedes all other practices and documentation. Amendments require:
1. Documentation of rationale and impact
2. Approval by project lead
3. Version bump following semantic versioning
4. Migration plan for existing work
5. Propagation updates to dependent templates

All pull requests and reviews MUST verify compliance with this constitution. Complexity that violates constraints MUST be explicitly justified in the Architectural Decision Record (ADR).

Compliance review occurs at every checkpoint in the development workflow. Non-compliant code MUST NOT be merged.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
