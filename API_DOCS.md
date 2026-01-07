# Multi-User Todo API Documentation

This document provides detailed examples for using the Multi-User Todo API with proper authentication.

## Base URL
```
http://localhost:8000/api
```

## Authentication Flow

### 1. Signup
Create a new user account and receive a JWT token:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "id": "user-id-here",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2026-01-07T12:00:00.000000",
  "updated_at": "2026-01-07T12:00:00.000000"
}
```

### 2. Signin
Sign in with existing credentials and receive a JWT token:

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "id": "user-id-here",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2026-01-07T12:00:00.000000",
  "updated_at": "2026-01-07T12:00:00.000000"
}
```

## Protected Endpoints

All protected endpoints require the Authorization header in the format:
```
Authorization: Bearer <JWT_TOKEN>
```

### Tasks API

#### List Tasks
```bash
curl -X GET "http://localhost:8000/api/{USER_ID}/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Create Task
```bash
curl -X POST http://localhost:8000/api/{USER_ID}/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "New Task",
    "description": "Task description (optional)"
  }'
```

#### Get Single Task
```bash
curl -X GET http://localhost:8000/api/{USER_ID}/tasks/{TASK_ID} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update Task
```bash
curl -X PUT http://localhost:8000/api/{USER_ID}/tasks/{TASK_ID} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated description"
  }'
```

#### Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/api/{USER_ID}/tasks/{TASK_ID}/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Delete Task
```bash
curl -X DELETE http://localhost:8000/api/{USER_ID}/tasks/{TASK_ID} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Error Responses

### Missing Authorization Header
```
Status: 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "missing",
      "loc": ["header", "Authorization"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

### Invalid Token
```
Status: 401 Unauthorized
{
  "detail": "Invalid token"
}
```

### Unauthorized Access (Different User ID)
```
Status: 404 Not Found
{
  "detail": "User not found"
}
```

## Important Notes

1. **Token Format**: Always use `Authorization: Bearer <TOKEN>` format
2. **User ID Matching**: The `{USER_ID}` in the URL must match the user ID in the JWT token
3. **Token Expiration**: JWT tokens expire after 7 days
4. **Security**: Never share tokens or expose them in client-side code publicly