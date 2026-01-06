# Task API Contract

**Date**: 2026-01-06
**Feature**: Multi-User Todo Web Application
**Version**: 1.0.0

## Overview

Task management endpoints provide CRUD operations (Create, Read, Update, Delete, Toggle) for user's personal tasks. All endpoints require JWT authentication and enforce user data isolation by scoping resources to `user_id`.

## Base URL

```
https://localhost:8000/api/{user_id}/tasks
```

**Note**: `user_id` must match JWT token `sub` claim. Mismatch returns 404 Not Found.

## Authentication

All endpoints require valid JWT token in Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Ownership Verification**:

- `user_id` in URL path must match JWT token `sub` claim
- All operations verify: `task.user_id == authenticated_user.id`
- Mismatch returns 404 Not Found (not 401) for security

---

## Endpoints

### GET /{user_id}/tasks

List all tasks belonging to authenticated user.

**URL Parameter**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |

**Query Parameters** (optional):

| Parameter | Type | Default | Description |
|-----------|--------|----------|-------------|
| limit | integer | 50 | Maximum tasks to return |
| offset | integer | 0 | Pagination offset |

**Success Response (200 OK)**:

```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-4266141740000",
      "user_id": "550e8400-e29b-41d4-a716-446655440174",
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "completed": false,
      "created_at": "2026-01-06T10:00:00Z",
      "updated_at": "2026-01-06T10:00:00Z"
    },
    {
      "id": "987f6543-e21b-43d3-b789-555555666666",
      "user_id": "550e8400-e29b-41d4-a716-446655440174",
      "title": "Walk the dog",
      "description": null,
      "completed": true,
      "created_at": "2026-01-05T15:00:00Z",
      "updated_at": "2026-01-06T08:00:00Z"
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

**Response Fields**:

| Field | Type | Description |
|-------|--------|-------------|
| tasks | array | List of task objects |
| total | integer | Total count of user's tasks |
| limit | integer | Maximum tasks in response (from query) |
| offset | integer | Pagination offset (from query) |

**Ordering**: Tasks sorted by `created_at DESC` (newest first). Completed tasks appear after pending tasks.

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "User not found"}` | user_id doesn't match token sub |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Performance**: <100ms for 100 tasks (with indexes on user_id + created_at)

---

### POST /{user_id}/tasks

Create new task for authenticated user.

**URL Parameter**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |

**Request Body**:

```json
{
  "title": "New task title",
  "description": "Optional description"
}
```

**Request Fields**:

| Field | Type | Required | Validation | Description |
|-------|--------|-----------|--------------|-------------|
| title | string | Yes | 1-200 characters |
| description | string (text) | No | 0-1000 characters |

**Success Response (201 Created)**:

```json
{
  "id": "abc12345-def6-7890-abcd-123456789012",
  "user_id": "550e8400-e29b-41d4-a716-446655440174",
  "title": "New task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-06T12:00:00Z",
  "updated_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 400 Bad Request | `{"error": "Title is required and must be 1-200 characters"}` | Title missing or invalid length |
| 400 Bad Request | `{"error": "Description must be under 1000 characters"}` | Description too long |
| 400 Bad Request | `{"error": "Maximum task limit reached (1000 tasks per user)"}` | User exceeded task limit |
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "User not found"}` | user_id doesn't match token sub |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Performance**: <50ms to create and return task

---

### GET /{user_id}/tasks/{task_id}

Get single task by ID.

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |
| task_id | string (UUID) | Yes | Task ID to retrieve |

**Success Response (200 OK)**:

```json
{
  "id": "abc12345-def6-7890-abcd-123456789012",
  "user_id": "550e8400-e29b-41d4-a716-446655440174",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "Task not found"}` | Task doesn't exist OR user_id mismatch (ownership violation) |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Security Note**: Returns 404 (not 401) for ownership violations to prevent task enumeration.

**Performance**: <10ms to retrieve single task by primary key

---

### PUT /{user_id}/tasks/{task_id}

Update existing task (title and/or description).

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |
| task_id | string (UUID) | Yes | Task ID to update |

**Request Body**:

```json
{
  "title": "Updated task title",
  "description": "Updated description"
}
```

**Request Fields**:

| Field | Type | Required | Validation | Description |
|-------|--------|-----------|--------------|-------------|
| title | string | No* | 1-200 characters (if provided) |
| description | string (text) | No* | 0-1000 characters (if provided) |

\* At least one field (title OR description) must be provided.

**Success Response (200 OK)**:

```json
{
  "id": "abc12345-def6-7890-abcd-123456789012",
  "user_id": "550e8400-e29b-41d4-a716-446655440174",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T13:00:00Z"
}
```

**Note**: `updated_at` timestamp automatically updated to current time.

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 400 Bad Request | `{"error": "At least one field (title or description) required"}` | No fields provided |
| 400 Bad Request | `{"error": "Title must be 1-200 characters"}` | Title invalid length |
| 400 Bad Request | `{"error": "Description must be under 1000 characters"}` | Description too long |
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "Task not found"}` | Task doesn't exist OR user_id mismatch |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Performance**: <50ms to update task (primary key lookup + update)

---

### DELETE /{user_id}/tasks/{task_id}

Delete task permanently.

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |
| task_id | string (UUID) | Yes | Task ID to delete |

**Request Body**: None

**Success Response (200 OK)**:

```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "Task not found"}` | Task doesn't exist OR user_id mismatch |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Security Note**: Returns 404 (not 401) for ownership violations.

**Performance**: <50ms to delete task (primary key lookup + delete)

---

### PATCH /{user_id}/tasks/{task_id}/complete

Toggle task completion status between complete and incomplete.

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|-----------|-------------|
| user_id | string (UUID) | Yes | User ID from JWT `sub` claim |
| task_id | string (UUID) | Yes | Task ID to toggle |

**Request Body**: None

**Success Response (200 OK)**:

```json
{
  "id": "abc12345-def6-7890-abcd-123456789012",
  "user_id": "550e8400-e29b-41d4716-446655440174",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": true,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T14:30:00Z"
}
```

**Note**: `completed` toggled to opposite value. `updated_at` timestamp updated.

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 401 Unauthorized | `{"error": "Authorization required"}` | JWT token missing or invalid |
| 404 Not Found | `{"error": "Task not found"}` | Task doesn't exist OR user_id mismatch |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Performance**: <50ms to toggle completion (primary key lookup + update)

---

## User Data Isolation

### Query Pattern

All task queries filter by authenticated user ID:

```sql
SELECT * FROM tasks
WHERE user_id = :authenticated_user_id
ORDER BY created_at DESC;
```

**Database Index**: `CREATE INDEX tasks_user_id_idx ON tasks(user_id)`

### Ownership Verification

For update/delete operations:

```python
# 1. Fetch task by ID
task = await session.get(Task, task_id)

# 2. Verify ownership
if task.user_id != authenticated_user_id:
    raise HTTPException(status_code=404, detail="Task not found")

# 3. Proceed with operation
# ... perform update or delete
```

**Security**: Returns 404 Not Found (not 401) for ownership violations to prevent task enumeration.

---

## Pagination Strategy

When user has many tasks (>50), use pagination:

**First page**:
```
GET /{user_id}/tasks?limit=50&offset=0
```

**Second page**:
```
GET /{user_id}/tasks?limit=50&offset=50
```

**Response includes**:
- `tasks`: Array of task objects
- `total`: Total count of user's tasks
- `limit`: Maximum tasks per page
- `offset`: Current page offset

**Client logic**:
```javascript
if (tasks.length < total) {
  // Show "Load More" button
  nextOffset = offset + limit;
}
```

---

## Performance Targets

| Operation | Target | With Indexes |
|-----------|--------|--------------|
| List 100 tasks | <100ms | ✅ user_id + created_at index |
| Get single task | <10ms | ✅ Primary key |
| Create task | <50ms | ✅ Foreign key validation |
| Update task | <50ms | ✅ Primary key lookup |
| Delete task | <50ms | ✅ Primary key lookup |
| Toggle completion | <50ms | ✅ Primary key lookup |

---

## Testing Scenarios

### List Tasks - Happy Path

**Request**:

```bash
curl -X GET http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440174/tasks \
  -H "Authorization: Bearer <token>"
```

**Expected Response**: 200 OK with user's tasks ordered newest first

### Create Task - Happy Path

**Request**:

```bash
curl -X POST http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440174/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Optional description"
  }'
```

**Expected Response**: 201 Created with task ID

### Update Task - Happy Path

**Request**:

```bash
curl -X PUT http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440174/tasks/abc12345-def6-7890-abcd-123456789012 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title"
  }'
```

**Expected Response**: 200 OK with updated task (updated_at changed)

### Delete Task - Happy Path

**Request**:

```bash
curl -X DELETE http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440174/tasks/abc12345-def6-7890-abcd-123456789012 \
  -H "Authorization: Bearer <token>"
```

**Expected Response**: 200 OK with success message

### Toggle Completion - Happy Path

**Request**:

```bash
curl -X PATCH http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440174/tasks/abc12345-def6-7890-abcd-123456789012/complete \
  -H "Authorization: Bearer <token>"
```

**Expected Response**: 200 OK with completed status toggled

### Cross-User Access - Security Test

**Request**:

```bash
# User A (ID: 550e8400...) has task ID: abc12345...
# User B (ID: 99988888...) attempts to access User A's task

curl -X GET http://localhost:8000/api/99988888-.../tasks/abc12345... \
  -H "Authorization: Bearer <user_B_token>"
```

**Expected Response**: 404 Not Found (ownership violation)

---

## References

- [Data Model](../data-model.md) - Entity definitions
- [Auth API Contract](auth-api.md) - Authentication endpoints
- [Errors Contract](errors.md) - Standard error format
- [Research](../research.md) - Technical decisions
- [Specification](../spec.md) - Functional requirements
