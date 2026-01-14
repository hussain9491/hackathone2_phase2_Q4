# Implementation Plan: Phase III Todo AI Chatbot

**Branch**: `001-multi-user-todo` | **Date**: 2026-01-13 | **Spec**: [specs/001-multi-user-todo/spec.md](specs/001-multi-user-todo/spec.md)
**Input**: Feature specification from `/specs/[001-multi-user-todo]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a conversational AI interface that allows users to manage their tasks through natural language chat, powered by Google's Gemini API and MCP (Model Context Protocol) tools, with a completely stateless backend architecture. The AI chatbot enables users to create, list, complete, update, and delete tasks through natural conversation while maintaining all security and data isolation properties of the existing application.

## Technical Context

**Language/Version**: Python 3.9+, TypeScript 5.3+ strict mode, Next.js 16+
**Primary Dependencies**: FastAPI 0.109+, SQLModel 0.0.14+, Google Gemini API, MCP SDK, google-generativeai
**Storage**: Neon Serverless PostgreSQL with conversations and messages tables
**Testing**: pytest for backend, none for this phase (manual testing)
**Target Platform**: Web application (Linux/Windows server, any modern browser)
**Project Type**: Web application with frontend and backend
**Performance Goals**: API responses <200ms for all operations, frontend load <2s on 3G
**Constraints**: <200ms p95 for all API operations, JWT 7-day expiration, bcrypt cost 12
**Scale/Scope**: 1000+ concurrent users, 100+ messages per conversation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Authentication Required**: Every API endpoint (except signup/signin) MUST verify JWT token. All new chat endpoints follow this requirement.
2. **User Isolation**: All database queries MUST filter by authenticated user ID. New conversation and message queries enforce user isolation.
3. **No Manual Coding**: All code changes MUST originate from specs → plan → tasks workflow. Following spec-driven approach.
4. **Type Safety**: TypeScript strict mode and Python type hints MUST be enforced. Both frontend and backend maintain strict typing.
5. **Environment Variables**: All secrets and configuration MUST use environment variables. GEMINI_API_KEY stored in environment.
6. **HTTP Standards**: API endpoints MUST use appropriate status codes. Following standard HTTP practices.
7. **Timestamps**: All database records MUST include created_at and updated_at. New tables include proper timestamps.
8. **Foreign Keys**: All relationships MUST use foreign key constraints. New tables maintain proper relationships with users table.
9. **CORS Configuration**: CORS MUST be properly configured. Using existing CORS setup.
10. **Password Hashing**: Passwords MUST use industry-standard hashing algorithm. Using existing bcrypt implementation.

## Project Structure

### Documentation (this feature)
```text
specs/001-multi-user-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py           # Existing task model
│   │   ├── user.py           # Existing user model
│   │   ├── conversation.py   # New conversation model (Phase III)
│   │   └── message.py        # New message model (Phase III)
│   ├── services/
│   │   ├── task_service.py   # Existing task service
│   │   └── chat_service.py   # New chat service (Phase III)
│   ├── routers/
│   │   ├── auth.py           # Existing auth router
│   │   ├── tasks.py          # Existing tasks router
│   │   └── chat.py           # New chat router (Phase III)
│   ├── chatbot/              # New chatbot module (Phase III)
│   │   ├── simple_agent.py   # AI agent implementation
│   │   ├── mcp_server.py     # MCP tools server
│   │   └── tools/            # MCP tools definitions
│   └── main.py               # Main application (includes chat router)
└── tests/

frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/page.tsx # Existing dashboard
│   │   └── chat/page.tsx      # New chat page (Phase III)
│   ├── components/
│   │   ├── auth-provider.tsx   # Existing auth provider
│   │   ├── task-form.tsx       # Existing task form
│   │   ├── task-list.tsx       # Existing task list
│   │   └── ui/                 # UI components
│   └── lib/
│       ├── auth-client.ts     # Existing auth client
│       └── api-client.ts      # Extended to include chat API calls
└── tests/
```

**Structure Decision**: Selected web application structure with separate backend and frontend. Added new conversation and message models to backend, new chat service and router, new chatbot module with AI agent and MCP tools. Added new chat page to frontend with navigation between dashboard and chat interfaces.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional database tables | Need to store conversation history for AI chatbot | Would compromise stateless architecture requirement |
| New API endpoints | Required for chat functionality | Would prevent users from accessing AI features |
| Third-party AI service integration | Essential for natural language processing | Would limit functionality to basic CRUD operations |
