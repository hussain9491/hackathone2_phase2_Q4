# Authentication API Contract

**Date**: 2026-01-06
**Feature**: Multi-User Todo Web Application
**Version**: 1.0.0

## Overview

Authentication endpoints enable user account creation and JWT token generation. These are the only public endpoints (no authentication required). All other endpoints require JWT token in `Authorization: Bearer <token>` header.

## Base URL

```
https://localhost:8000/api
```

## Endpoints

### POST /auth/signup

Create new user account with email and password.

**Request**:

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Fields**:

| Field | Type | Required | Validation | Description |
|--------|--------|-----------|-------------|
| email | string | Yes | Valid email format, max 255 chars, unique in database |
| password | string | Yes | Minimum 8 characters |

**Success Response (201 Created)**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440174",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2026-01-06T12:00:00Z",
  "updated_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 400 Bad Request | `{"error": "Invalid email format"}` | Email doesn't match regex |
| 400 Bad Request | `{"error": "Password must be at least 8 characters"}` | Password too short |
| 409 Conflict | `{"error": "Email already registered"}` | Email already exists in database |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Behavior**:
- Password hashed using bcrypt (cost factor 12) before storage
- User record created in `users` table
- JWT token generated with 7-day expiry
- Token claims: `sub` (user_id), `email`, `exp` (expiry timestamp), `iat` (issued at)

---

### POST /auth/signin

Authenticate existing user and receive JWT token.

**Request**:

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Fields**:

| Field | Type | Required | Validation | Description |
|--------|--------|-----------|-------------|
| email | string | Yes | Valid email format |
| password | string | Yes | Any string (comparison against hashed value) |

**Success Response (200 OK)**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440174",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2026-01-06T12:00:00Z",
  "updated_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses**:

| Status | Error | Description |
|--------|--------|-------------|
| 400 Bad Request | `{"error": "Invalid email format"}` | Email doesn't match regex |
| 401 Unauthorized | `{"error": "Invalid email or password"}` | Email not found or password incorrect |
| 500 Internal Server Error | `{"error": "Internal server error"}` | Unexpected server error |

**Security Note**: Error message doesn't reveal which field is incorrect (email vs password) to prevent account enumeration.

**Behavior**:
- Password verified using bcrypt compare against stored hash
- JWT token generated with 7-day expiry from current time
- Token identical to signup response format
- User `updated_at` timestamp updated on successful signin

---

## JWT Token Format

**Header**:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440174",
  "email": "user@example.com",
  "iat": 1704556800,
  "exp": 1705162800
}
```

**Claims**:

| Claim | Type | Description |
|-------|--------|-------------|
| sub (subject) | string (UUID) | User ID from users.id |
| email | string | User email from users.email |
| iat (issued at) | integer (timestamp) | Unix timestamp when token issued |
| exp (expiration) | integer (timestamp) | Unix timestamp when token expires (iat + 604800 = 7 days) |

**Signature**: HMAC-SHA256 using `BETTER_AUTH_SECRET` environment variable (minimum 32 characters)

---

## Authentication Flow

### Signup Flow

```
Client                           Server
  │                                 │
  ├─ POST /auth/signup ─────────► │
  │    {email, password}            │
  │                                 │ Validate email format
  │                                 │ Validate password length
  │                                 │ Check email uniqueness
  │                                 │ Hash password (bcrypt cost 12)
  │                                 │ Create user record
  │                                 │ Generate JWT (7-day expiry)
  │  ◄───────────────────────────┤
  │    {id, email, token, timestamps}│
  │                                 │
  ├─ Store token in cookie            │
  │    (httpOnly, secure)            │
  │                                 │
  └─ Redirect to /dashboard          │
```

### Signin Flow

```
Client                           Server
  │                                 │
  ├─ POST /auth/signin ───────────► │
  │    {email, password}            │
  │                                 │ Validate email format
  │                                 │ Find user by email
  │                                 │ Compare password hash (bcrypt)
  │                                 │ Generate JWT (7-day expiry)
  │                                 │ Update user.updated_at
  │  ◄─────────────────────────────┤
  │    {id, email, token, timestamps}│
  │                                 │
  ├─ Store token in cookie            │
  │    (httpOnly, secure)            │
  │                                 │
  └─ Redirect to /dashboard          │
```

---

## Token Usage

All protected endpoints require JWT token in Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Validation** (for all protected endpoints):

1. Extract token from `Authorization` header
2. Verify token signature using `BETTER_AUTH_SECRET`
3. Check token expiration (`exp` > current time)
4. Extract `user_id` from `sub` claim
5. Verify user exists in database
6. Proceed with request if all checks pass

**Token Expiry Handling**:

| Scenario | Status | Response |
|----------|--------|----------|
| Token expired (`exp` < current time) | 401 Unauthorized | `{"error": "Token expired"}` |
| Token invalid signature | 401 Unauthorized | `{"error": "Invalid token"}` |
| Token missing | 401 Unauthorized | `{"error": "Authorization required"}` |
| Token valid | 200 OK | Process request normally |

---

## Security Considerations

### Password Hashing

- **Algorithm**: bcrypt
- **Cost Factor**: 12
- **Salt**: Automatic (bcrypt handles)
- **Reasoning**: Balances security and performance; cost factor 12 requires ~200ms for hash (acceptable for signup/signin)

### Token Storage

- **Frontend**: Store in httpOnly, Secure cookie (not localStorage)
- **Lifetime**: 7 days (604800 seconds)
- **Transport**: HTTPS in production (SSL/TLS)

### CORS Configuration

- **Development**: `http://localhost:3000`
- **Production**: Specific frontend domain(s)
- **Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization

### Rate Limiting (Future Enhancement)

- Not included in Phase II
- Recommend: 10 requests/minute per IP
- Prevents: Brute force attacks, account enumeration

---

## Testing Scenarios

### Signup - Happy Path

**Request**:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected Response**: 201 Created with user ID and JWT token

### Signup - Duplicate Email

**Request**:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected Response**: 409 Conflict with "Email already registered"

### Signin - Happy Path

**Request**:

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected Response**: 200 OK with user ID and JWT token

### Signin - Invalid Credentials

**Request**:

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "wrongpassword"
  }'
```

**Expected Response**: 401 Unauthorized with "Invalid email or password"

---

## References

- [Data Model](../data-model.md) - Entity definitions
- [Research](../research.md) - Technical decisions
- [Specification](../spec.md) - Functional requirements
