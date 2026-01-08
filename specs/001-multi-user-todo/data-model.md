# Data Model: Multi-User Todo Web Application

## Entities

### User
Represents an application user account with authentication credentials.

**Fields**:
- `id` (UUID/string): Unique identifier for the user
- `email` (string): User's email address (unique, indexed)
- `hashed_password` (string): BCrypt hashed password (255 characters max)
- `created_at` (datetime): Timestamp when account was created
- `updated_at` (datetime): Timestamp when account was last updated

**Relationships**:
- One-to-many: User has many Tasks (cascade delete)

**Validation Rules**:
- Email must follow standard email format
- Email must be unique across all users
- Email length: 5-255 characters
- Password must be at least 8 characters (before hashing)

### Task
Represents a todo item belonging to a specific user with title, description, and completion status.

**Fields**:
- `id` (UUID/string): Unique identifier for the task
- `user_id` (UUID/string): Foreign key to User entity
- `title` (string): Task title (required, 1-200 characters)
- `description` (string): Optional task description (0-1000 characters)
- `completed` (boolean): Whether the task is completed (default: false)
- `created_at` (datetime): Timestamp when task was created
- `updated_at` (datetime): Timestamp when task was last updated

**Relationships**:
- Many-to-one: Task belongs to one User (foreign key constraint)

**Validation Rules**:
- Title is required and must be 1-200 characters
- Description is optional and must be 0-1000 characters
- User ID must reference an existing user
- Completed defaults to false

**State Transitions**:
- Created with `completed = false`
- Can be toggled between `completed = true` and `completed = false` multiple times
- Can be updated (title/description) while maintaining completion status

### Session (Implicit)
Represents user authentication state through JWT token.

**Claims**:
- `sub` (string): User ID (subject of the token)
- `email` (string): User's email address
- `exp` (number): Expiration timestamp (7 days from creation)
- `iat` (number): Issued at timestamp

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_users_email ON users(email);
```

## Constraints

1. **Referential Integrity**: All tasks must belong to an existing user (foreign key constraint)
2. **Cascade Deletion**: When a user is deleted, all their tasks are automatically deleted
3. **Uniqueness**: Email addresses must be unique across all users
4. **Data Validation**: Field length and type constraints enforced at database level
5. **Timestamps**: All records have creation and update timestamps automatically managed