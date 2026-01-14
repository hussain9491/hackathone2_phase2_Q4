# Chat API Contract: Todo AI Chatbot

## Overview
Contract for the natural language task management API endpoint that allows users to interact with their todo list through conversational interface.

## Endpoint: POST /api/{user_id}/chat

### Description
Processes natural language messages from users and performs task management operations using AI-powered intent recognition and MCP tools. Maintains conversation context and persists all interactions to the database.

### Authentication
- JWT Bearer token required in Authorization header
- Token must be valid and not expired
- User ID in URL path must match authenticated user

### Request

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | The ID of the user making the request (must match JWT token) |

#### Headers
| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| Authorization | Bearer {token} | Yes | Valid JWT token for the requesting user |
| Content-Type | application/json | Yes | Request body format |

#### Body Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| conversation_id | integer | No | null | ID of existing conversation (null for new conversation) |
| message | string | Yes | - | Natural language message from user |

##### Example Request Body
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

### Response

#### Success Response (200 OK)
| Field | Type | Description |
|-------|------|-------------|
| conversation_id | integer | ID of the conversation (newly created or existing) |
| response | string | AI-generated response to the user's message |
| tool_calls | array | Array of tool calls made during processing |

##### Tool Call Object
| Field | Type | Description |
|-------|-----|-------------|
| tool | string | Name of the MCP tool called |
| parameters | object | Parameters passed to the tool |
| result | object | Result returned by the tool |

##### Example Success Response
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your tasks.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "Buy groceries"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Buy groceries",
        "message": "Task created successfully"
      }
    }
  ]
}
```

#### Error Responses

##### 400 Bad Request
Returned when request parameters are invalid.

```json
{
  "detail": "Invalid request parameters",
  "code": "INVALID_REQUEST"
}
```

##### 401 Unauthorized
Returned when authentication token is missing, invalid, or expired.

```json
{
  "detail": "Not authenticated",
  "code": "NOT_AUTHENTICATED"
}
```

##### 403 Forbidden
Returned when user tries to access another user's chat endpoint.

```json
{
  "detail": "Cannot access chat for different user",
  "code": "FORBIDDEN_ACCESS"
}
```

##### 404 Not Found
Returned when conversation_id doesn't exist or doesn't belong to the user.

```json
{
  "detail": "Conversation not found",
  "code": "CONVERSATION_NOT_FOUND"
}
```

##### 500 Internal Server Error
Returned when an unexpected error occurs during processing.

```json
{
  "detail": "Internal server error",
  "code": "INTERNAL_ERROR"
}
```

### MCP Tools Used

This endpoint utilizes the following MCP tools for task operations:

#### add_task
- **Purpose**: Create a new task
- **Parameters**: `{user_id: string, title: string, description?: string}`
- **Returns**: `{task_id: number, status: string, title: string, message: string}`

#### list_tasks
- **Purpose**: Retrieve user's tasks
- **Parameters**: `{user_id: string, status?: "all"|"pending"|"completed"}`
- **Returns**: `{tasks: array, count: number, status_filter: string, message: string}`

#### complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: `{user_id: string, task_id: string}`
- **Returns**: `{task_id: number, status: string, title: string, message: string}`

#### delete_task
- **Purpose**: Delete a task
- **Parameters**: `{user_id: string, task_id: string}`
- **Returns**: `{task_id: number, status: string, message: string}`

#### update_task
- **Purpose**: Update task details
- **Parameters**: `{user_id: string, task_id: string, title?: string, description?: string}`
- **Returns**: `{task_id: number, status: string, title: string, message: string}`

### State Management
- All conversation state is persisted to database
- Each request loads full conversation history from database
- Responses are saved to database after processing
- Server maintains no in-memory conversation state
- Conversation history is used for context in subsequent messages

### Performance Requirements
- API response time: < 3 seconds (95th percentile)
- Tool execution time: < 200ms per tool
- Database operations: < 100ms
- Message persistence: < 50ms