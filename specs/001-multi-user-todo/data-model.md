# Data Model: Multi-User Todo Web Application with AI Chatbot

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
- One-to-many: User has many Conversations (cascade delete)
- One-to-many: User has many Messages (cascade delete)

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

### Conversation
Represents a single conversation between a user and the AI assistant.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing identifier for the conversation
- `user_id` (String): Foreign key linking conversation to the owning user
- `created_at` (DateTime): Timestamp when conversation was created
- `updated_at` (DateTime): Timestamp when conversation was last updated

**Relationships**:
- Belongs to one User (user_id → users.id)
- Has many Messages (one-to-many with messages table)

**Validation Rules**:
- `user_id` must exist in users table
- `user_id` cannot be null
- `created_at` defaults to current timestamp
- `updated_at` defaults to current timestamp

### Message
Represents a single message in a conversation (either from user or AI assistant).

**Fields**:
- `id` (Integer): Primary key, auto-incrementing identifier for the message
- `conversation_id` (Integer): Foreign key linking message to its conversation
- `user_id` (String): Foreign key linking message to the user who sent it
- `role` (String): Enum indicating if message is from "user" or "assistant"
- `content` (Text): The actual content of the message
- `tool_calls` (JSON): Optional array of tool calls made during processing
- `created_at` (DateTime): Timestamp when message was created

**Relationships**:
- Belongs to one Conversation (conversation_id → conversations.id)
- Belongs to one User (user_id → users.id)

**Validation Rules**:
- `conversation_id` must exist in conversations table
- `user_id` must exist in users table
- `role` must be either "user" or "assistant"
- `content` cannot be null or empty
- `tool_calls` must be valid JSON if provided
- `created_at` defaults to current timestamp

## State Transitions

### Task State Transitions
- Created with `completed = false`
- Can be toggled between `completed = true` and `completed = false` multiple times
- Can be updated (title/description) while maintaining completion status

### Conversation State Transitions
- New conversation created when user starts chatting
- Updated when new messages are added to the conversation
- No explicit end state (conversations persist indefinitely in Phase III)

### Message State Transitions
- New message created when user sends a message
- Assistant response message created after AI processing
- No state changes after creation (messages are immutable)

## Database Schema

```sql
-- Users table (existing)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Tasks table (existing)
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Conversations table (new for Phase III)
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Messages table (new for Phase III)
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (role IN ('user', 'assistant'))
);

-- Indexes (existing + new)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## Constraints

1. **Referential Integrity**: All tasks, conversations, and messages must belong to an existing user (foreign key constraint)
2. **Cascade Deletion**: When a user is deleted, all their tasks, conversations, and messages are automatically deleted
3. **Uniqueness**: Email addresses must be unique across all users
4. **Data Validation**: Field length and type constraints enforced at database level
5. **Timestamps**: All records have creation and update timestamps automatically managed
6. **User Isolation**: All queries must be scoped to authenticated user ID to prevent cross-user access
7. **Message Roles**: Message roles must be either "user" or "assistant" (enforced by CHECK constraint)