# Error Response Format Contract

**Date**: 2026-01-06
**Feature**: Multi-User Todo Web Application
**Version**: 1.0.0

## Overview

All API endpoints return errors in consistent JSON format. This contract defines standard error responses across authentication and task management endpoints.

## Error Response Format

All error responses follow this structure:

```json
{
  "error": "Human-readable error message"
}
```

**Fields**:

| Field | Type | Always Present | Description |
|-------|--------|-----------------|-------------|
| error | string | Yes | Clear, actionable error message for users |

**No additional fields**: Simplified error handling for frontend consistency.

---

## HTTP Status Codes

### Success Codes

| Status | Usage | Endpoint(s) |
|--------|---------|--------------|
| 200 OK | Successful operation (except creation) | GET (list, single), PUT (update), DELETE, PATCH (toggle) |
| 201 Created | Resource created successfully | POST (signup, signin, create task) |

### Client Error Codes

| Status | Usage | Common Errors |
|--------|---------|---------------|
| 400 Bad Request | Invalid request data | Invalid email format, password too short, title too long, validation failures |
| 401 Unauthorized | Authentication missing or invalid | Token missing, token expired, invalid token, signature verification failed |
| 403 Forbidden | Access denied (not used in this phase) | Future: permission checks |
| 404 Not Found | Resource doesn't exist OR ownership violation | Task/user not found, cross-user access attempts |
| 409 Conflict | Resource conflict | Email already registered |

### Server Error Codes

| Status | Usage | Common Errors |
|--------|---------|---------------|
| 500 Internal Server Error | Unexpected server error | Database connection failure, unhandled exceptions |

---

## Standard Error Messages

### Authentication Errors

| Error Message | Status | Context |
|--------------|--------|----------|
| "Authorization required" | 401 | JWT token missing from Authorization header |
| "Invalid token" | 401 | JWT token signature verification failed |
| "Token expired" | 401 | JWT token exp claim < current time |
| "Invalid email format" | 400 | Email doesn't match validation regex |
| "Password must be at least 8 characters" | 400 | Password too short (<8 chars) |
| "Email already registered" | 409 | Signup with existing email address |
| "Invalid email or password" | 401 | Signin credentials incorrect (security: don't reveal which) |

### Task Management Errors

| Error Message | Status | Context |
|--------------|--------|----------|
| "Title is required and must be 1-200 characters" | 400 | Create/update task with invalid title |
| "Description must be under 1000 characters" | 400 | Create/update task with description too long |
| "At least one field (title or description) required" | 400 | Update task with no fields provided |
| "Maximum task limit reached (1000 tasks per user)" | 400 | Create task exceeds user task limit |
| "Task not found" | 404 | Get/update/delete/toggle non-existent task OR ownership violation |
| "User not found" | 404 | user_id in URL doesn't match JWT sub claim |

### General Errors

| Error Message | Status | Context |
|--------------|--------|----------|
| "Internal server error" | 500 | Unexpected server failure, database error, unhandled exception |

---

## Error Handling Flow

### Frontend Error Handling

```typescript
// API client utility
async function apiRequest(url: string, options: RequestInit) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${getToken()}`,
      'Content-Type': 'application/json',
    },
  });

  // Handle non-success status codes
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error);
  }

  return response.json();
}

// Component usage
try {
  await createTask({ title: 'New task' });
} catch (error) {
  setError(error.message); // Display to user
}
```

### Error Display Strategy

| Status | UI Action | Example |
|--------|-----------|----------|
| 400 | Show inline validation error | "Title is required and must be 1-200 characters" |
| 401 | Redirect to signin page | Token expired/invalid - user redirected to authentication |
| 404 | Show "Not found" message | "Task not found" or "User not found" |
| 409 | Show conflict error | "Email already registered" |
| 500 | Show generic error + retry option | "Service temporarily unavailable. Please try again." |

---

## Security Considerations

### 401 vs 404 for Ownership Violations

**Decision**: Return 404 Not Found (not 401 Unauthorized) for cross-user access attempts.

**Rationale**:
- 401 reveals resource exists (user can enumerate tasks by trying different IDs)
- 404 reveals nothing (prevents task enumeration)
- Follows security best practice: "Don't reveal what you don't own"

**Implementation**:

```python
# Wrong - reveals task exists
if task.user_id != authenticated_user_id:
    raise HTTPException(status_code=401, detail="Unauthorized")

# Correct - hides task existence
if task.user_id != authenticated_user_id:
    raise HTTPException(status_code=404, detail="Task not found")
```

### Generic Error Messages

**Decision**: Use specific, actionable error messages (not generic "Error 500").

**Examples**:
- ✅ "Email already registered" (specific)
- ❌ "Error occurred" (generic)
- ✅ "Title is required and must be 1-200 characters" (actionable)
- ❌ "Validation failed" (generic)

### Error Logging (Backend)

```python
import logging
logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        f"HTTP {exc.status_code}: {exc.detail}",
        extra={"path": str(request.url), "method": request.method}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

---

## Rate Limiting (Future Enhancement)

Not included in Phase II, but recommended for production:

### Headers

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1704556900
```

### Error Response

```json
{
  "error": "Rate limit exceeded. Please try again later."
}
```

**Status**: 429 Too Many Requests

---

## Frontend Error State Management

### Error Categories

```typescript
type ApiError = {
  message: string;
  status: number;
  isAuthError: boolean;
  isValidationError: boolean;
};

function classifyError(status: number): Partial<ApiError> {
  if (status === 401) {
    return { isAuthError: true, shouldRedirect: true };
  }
  if (status === 400) {
    return { isValidationError: true };
  }
  return {};
}
```

### Global Error Boundary (Next.js)

```typescript
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  // Check if auth error
  if (error.message.includes('Authorization required')) {
    return <Redirect to="/signin" />;
  }

  // Show error page
  return (
    <div>
      <h1>Something went wrong</h1>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

---

## Testing Checklist

### Error Scenarios to Test

- [ ] Valid email format rejected with 400 + "Invalid email format"
- [ ] Short password rejected with 400 + "Password must be at least 8 characters"
- [ ] Duplicate email rejected with 409 + "Email already registered"
- [ ] Invalid signin credentials rejected with 401 + "Invalid email or password"
- [ ] Missing token rejected with 401 + "Authorization required"
- [ ] Expired token rejected with 401 + "Token expired"
- [ ] Task title too long rejected with 400 + specific message
- [ ] Task description too long rejected with 400 + specific message
- [ ] Update task with no fields rejected with 400 + "At least one field required"
- [ ] Cross-user access returns 404 + "Task not found"
- [ ] Non-existent task returns 404 + "Task not found"
- [ ] Database error returns 500 + "Internal server error"

---

## References

- [Auth API Contract](auth-api.md) - Authentication-specific errors
- [Task API Contract](task-api.md) - Task-specific errors
- [Data Model](../data-model.md) - Entity definitions
- [Specification](../spec.md) - Functional requirements
