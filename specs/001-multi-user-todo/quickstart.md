# Quickstart Guide: Phase III Todo AI Chatbot

## Overview
This guide explains how to set up and run the Todo AI Chatbot application with natural language task management capabilities.

## Prerequisites
- Node.js 18+ or 20+
- Python 3.9+
- PostgreSQL database (Neon Serverless recommended)
- Google Gemini API key

## Setup Instructions

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL, BETTER_AUTH_SECRET, GEMINI_API_KEY, and CORS_ORIGINS
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET
```

### 4. Environment Variables

#### Backend (.env)
```env
# Neon PostgreSQL Database Connection
DATABASE_URL="postgresql://..."

# JWT Secret (generate a strong secret for production)
JWT_SECRET="your-secure-jwt-secret"

# Better Auth Configuration
BETTER_AUTH_SECRET="your-better-auth-secret"

BETTER_AUTH_URL=http://localhost:3004

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001

# Google Gemini API Key
GEMINI_API_KEY=your-gemini-api-key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3004
```

### 5. Initialize Database
```bash
cd backend
python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"
```

### 6. Run Applications

#### Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and get JWT token

### Tasks
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get single task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

### Chat
- `POST /api/{user_id}/chat` - Process natural language task requests

## Usage Examples

### 1. Sign up to get a token:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 2. Use the returned token to access tasks:
```bash
curl -X GET "http://localhost:8000/api/YOUR_USER_ID/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Create a new task:
```bash
curl -X POST http://localhost:8000/api/YOUR_USER_ID/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "New Task",
    "description": "Task description"
  }'
```

### 4. Chat with the AI assistant:
```bash
curl -X POST http://localhost:8000/api/YOUR_USER_ID/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "conversation_id": null,
    "message": "Add a task to buy groceries"
  }'
```

## Frontend Navigation
- Visit `http://localhost:3000` for the home page
- Sign up/sign in to access the dashboard
- Use the "Chat with AI" button to access the natural language task management interface
- Use the "Back to Dashboard" button to return to the traditional task management UI

## MCP Tools Architecture
The AI chatbot uses the following standardized MCP tools:
- `add_task`: Create a new task
- `list_tasks`: Show tasks (all, pending, or completed)
- `complete_task`: Mark a task as done
- `delete_task`: Remove a task
- `update_task`: Modify task title or description

## Stateless Architecture
- Server holds no conversation state in memory
- All conversation data persisted to database
- Each request loads full conversation history from database
- Server restarts do not lose conversation history
- Supports horizontal scaling

## Troubleshooting

### Common Issues
1. **API Key Issues**: Ensure GEMINI_API_KEY is set correctly
2. **Database Connection**: Verify DATABASE_URL is correct
3. **CORS Issues**: Check CORS_ORIGINS in .env file
4. **Authentication**: Verify JWT secrets are properly configured

### Development
- Frontend runs on `http://localhost:3000`
- Backend runs on `http://localhost:8000`
- API docs available at `http://localhost:8000/docs`
- Health check at `http://localhost:8000/health`