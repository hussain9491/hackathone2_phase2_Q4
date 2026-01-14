# Tasks: Phase III Todo AI Chatbot

**Feature**: Todo AI Chatbot - Natural Language Task Management
**Branch**: `001-multi-user-todo` | **Date**: 2026-01-13 | **Spec**: [specs/001-multi-user-todo/spec.md](specs/001-multi-user-todo/spec.md)

## Overview

Implementation of a conversational AI interface that allows users to manage their tasks through natural language chat, powered by Google's Gemini API and MCP (Model Context Protocol) tools, with a completely stateless backend architecture. The AI chatbot enables users to create, list, complete, update, and delete tasks through natural conversation while maintaining all security and data isolation properties of the existing application.

## Implementation Strategy

Build the AI chatbot feature incrementally, starting with foundational components and progressing to user-facing functionality. Begin with database schema extensions, then implement backend services and MCP tools, followed by the AI agent and API endpoint, and finally the frontend chat interface. Each phase builds upon the previous one while maintaining the existing functionality.

**MVP Scope**: Basic chat interface that can create tasks through natural language (User Story: Natural Language Task Creation)

## Dependencies

- User Story 1 (Authentication) - Required for user identification
- User Story 2 (Task Management) - Required for task operations
- User Story 3 (Data Isolation) - Required for security

**User Story Completion Order**:
1. Natural Language Task Creation (foundational functionality)
2. Natural Language Task Listing
3. Natural Language Task Modification
4. Natural Language Task Deletion
5. Conversation Continuity

## Parallel Execution Examples

**Per User Story**:
- Story 1: While implementing AI agent, simultaneously develop MCP tools and chat service
- Story 2: While building frontend chat UI, simultaneously implement backend API endpoint
- Story 3: While adding error handling, simultaneously implement logging and monitoring

---

## Phase 1: Setup

### Goal
Initialize project structure and dependencies for the AI chatbot implementation.

### Tasks
- [X] T101 Update requirements.txt with Google Gemini API and MCP dependencies in backend/requirements.txt
- [X] T102 [P] Add GEMINI_API_KEY to environment variables in .env and .env.example
- [X] T103 [P] Update frontend dependencies for chat interface in frontend/package.json

---

## Phase 2: Foundational

### Goal
Implement foundational database models and services required for all user stories.

### Tasks
- [X] T104 Create Conversation model in backend/src/models/conversation.py
- [X] T105 Create Message model in backend/src/models/message.py
- [X] T106 Update database initialization to include new models in backend/src/database.py
- [X] T107 [P] Create ChatService for conversation operations in backend/src/services/chat_service.py
- [X] T108 [P] Create MCP tools base structure in backend/src/chatbot/tools/__init__.py
- [X] T109 [P] Create MCP server structure in backend/src/chatbot/mcp_server.py

---

## Phase 3: Natural Language Task Creation

### Goal
Enable users to create tasks through natural language conversation.

### Independent Test Criteria
User can navigate to chat interface, type "Add a task to buy groceries", and see the task created in their task list via both traditional UI and chat responses.

### Tasks
- [X] T110 [US1] Create add_task MCP tool in backend/src/chatbot/tools/task_tools.py
- [X] T111 [P] [US1] Implement add_task functionality in MCP server backend/src/chatbot/mcp_server.py
- [X] T112 [P] [US1] Create SimpleTodoAgent for basic AI processing in backend/src/chatbot/simple_agent.py
- [X] T113 [US1] Create chat API endpoint in backend/src/routers/chat.py
- [X] T114 [P] [US1] Register chat endpoint in backend/src/main.py
- [X] T115 [P] [US1] Create basic chat page in frontend/src/app/chat/page.tsx
- [X] T116 [US1] Add chat navigation to dashboard in frontend/src/app/dashboard/page.tsx
- [X] T117 [P] [US1] Implement basic chat API client in frontend/src/lib/api-client.ts
- [X] T118 [US1] Test natural language task creation functionality

---

## Phase 4: Natural Language Task Listing

### Goal
Enable users to list tasks through natural language conversation.

### Independent Test Criteria
User can ask "Show me my tasks" or "What do I have to do?" and see their task list displayed in the chat interface.

### Tasks
- [X] T119 [US2] Create list_tasks MCP tool in backend/src/chatbot/tools/task_tools.py
- [X] T120 [P] [US2] Implement list_tasks functionality in MCP server backend/src/chatbot/mcp_server.py
- [X] T121 [P] [US2] Enhance SimpleTodoAgent to recognize listing intents in backend/src/chatbot/simple_agent.py
- [X] T122 [US2] Add conversation history loading to chat endpoint in backend/src/routers/chat.py
- [X] T123 [P] [US2] Enhance chat page with message history in frontend/src/app/chat/page.tsx
- [X] T124 [US2] Test natural language task listing functionality

---

## Phase 5: Natural Language Task Modification

### Goal
Enable users to complete and update tasks through natural language conversation.

### Independent Test Criteria
User can say "Mark task 1 as done" or "Update task 2 to 'Buy milk and eggs'" and see the changes reflected in their task list.

### Tasks
- [X] T125 [US3] Create complete_task MCP tool in backend/src/chatbot/tools/task_tools.py
- [X] T126 [P] [US3] Create update_task MCP tool in backend/src/chatbot/tools/task_tools.py
- [X] T127 [P] [US3] Implement complete_task and update_task in MCP server backend/src/chatbot/mcp_server.py
- [X] T128 [US3] Enhance SimpleTodoAgent to recognize completion/update intents in backend/src/chatbot/simple_agent.py
- [X] T129 [US3] Enhance chat page UI for task modification responses in frontend/src/app/chat/page.tsx
- [X] T130 [P] [US3] Test natural language task completion and update functionality

---

## Phase 6: Natural Language Task Deletion

### Goal
Enable users to delete tasks through natural language conversation.

### Independent Test Criteria
User can say "Delete task 1" or "Remove the grocery task" and see the task removed from their task list.

### Tasks
- [X] T131 [US4] Create delete_task MCP tool in backend/src/chatbot/tools/task_tools.py
- [X] T132 [P] [US4] Implement delete_task functionality in MCP server backend/src/chatbot/mcp_server.py
- [X] T133 [P] [US4] Enhance SimpleTodoAgent to recognize deletion intents in backend/src/chatbot/simple_agent.py
- [X] T134 [US4] Enhance chat page UI for task deletion responses in frontend/src/app/chat/page.tsx
- [X] T135 [P] [US4] Test natural language task deletion functionality

---

## Phase 7: Conversation Continuity

### Goal
Maintain conversation context across server restarts and provide stateless architecture.

### Independent Test Criteria
Server can restart without losing conversation history, and users can continue conversations seamlessly.

### Tasks
- [X] T136 [US5] Enhance chat endpoint to load full conversation history in backend/src/routers/chat.py
- [X] T137 [P] [US5] Implement conversation persistence in database in backend/src/services/chat_service.py
- [X] T138 [P] [US5] Add conversation ID management to frontend in frontend/src/app/chat/page.tsx
- [X] T139 [US5] Test server restart resilience with conversation continuity
- [X] T140 [P] [US5] Implement tool call logging in messages table in backend/src/chatbot/simple_agent.py

---

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Enhance user experience and add finishing touches.

### Tasks
- [X] T141 Improve chat UI/UX with typing indicators and better styling in frontend/src/app/chat/page.tsx
- [X] T142 [P] Add error handling and user-friendly messages in backend/src/chatbot/simple_agent.py
- [X] T143 [P] Add rate limiting to chat endpoint in backend/src/routers/chat.py
- [X] T144 Add loading states and error boundaries to frontend chat page in frontend/src/app/chat/page.tsx
- [X] T145 [P] Update documentation with chat API usage in README.md
- [X] T146 Test full AI chatbot functionality with multiple users
- [X] T147 [P] Optimize performance and fix any bugs found during testing
- [X] T148 Verify all security requirements are met for the chat functionality