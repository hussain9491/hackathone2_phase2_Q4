# Multi-User Todo Application

A secure multi-user todo web application with JWT authentication, PostgreSQL persistence, and complete user data isolation.

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript 5.3+ strict mode, Tailwind CSS 3.4+
- **Backend**: FastAPI 0.109+, SQLModel 0.0.14+, Python 3.9+
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT (7-day expiry, bcrypt cost 12)

## Setup

### Prerequisites

- Node.js 18+ or 20+
- Python 3.9+
- Neon PostgreSQL connection string

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL, BETTER_AUTH_SECRET, and CORS_ORIGINS

# Initialize database
python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"

# Run backend
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET

# Run frontend
npm run dev
```

## Features

- ✅ User account management (signup, signin)
- ✅ Task CRUD operations (create, read, update, delete, toggle)
- ✅ Complete data isolation between users
- ✅ Responsive UI (mobile 375px, desktop 1920px)
- ✅ JWT authentication with 7-day expiry
- ✅ bcrypt password hashing (cost factor 12)

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

### Authentication Requirements

All task endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

### Example Usage

**1. Sign up to get a token:**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**2. Use the returned token to access tasks:**
```bash
curl -X GET "http://localhost:8000/api/YOUR_USER_ID/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**3. Create a new task:**
```bash
curl -X POST http://localhost:8000/api/YOUR_USER_ID/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "New Task",
    "description": "Task description"
  }'
```

## Security

- JWT tokens expire after 7 days
- bcrypt password hashing with cost factor 12
- All protected routes require authentication
- Cross-user access returns 404 (not 401) for ownership violations
- CORS configured for frontend origin
- All secrets in environment variables (never in code)

## Performance

- API responses <200ms for all CRUD operations
- Database queries <100ms for 100 tasks
- Frontend initial load <2s on 3G connection
- Database indexes on user_id and created_at for fast queries

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry
│   ├── database.py           # Async DB connection
│   ├── auth.py              # JWT token generation
│   ├── models/              # SQLModel entities
│   ├── routers/             # API routes
│   ├── repositories/         # Data access layer
│   └── services/            # Business logic
└── requirements.txt

frontend/
├── src/
│   ├── app/                 # Next.js 16 app router
│   │   ├── page.tsx           # Home
│   │   ├── signin/page.tsx    # Signin page
│   │   ├── signup/page.tsx    # Signup page
│   │   ├── dashboard/page.tsx # Task management
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css        # Tailwind styles
│   │   └── proxy.ts          # Next.js 16 middleware
│   ├── components/
│   │   ├── auth-provider.tsx   # Auth context
│   │   ├── signup-form.tsx   # Signup form
│   │   ├── signin-form.tsx    # Signin form
│   │   ├── task-form.tsx      # Task creation form
│   │   ├── task-item.tsx      # Individual task display
│   │   ├── task-list.tsx      # Task list
│   │   └── ui/               # shadcn/ui components
│   └── lib/
│       ├── auth-client.ts     # JWT token utilities
│       └── api-client.ts      # API communication
└── .env.local                  # Frontend environment
```

## Development

- Frontend runs on `http://localhost:3000` (or `http://localhost:3001` if port 3000 is in use)
- Backend runs on `http://localhost:8000`
- API docs available at `http://localhost:8000/docs`
- Health check at `http://localhost:8000/health`

### CORS Configuration

The backend is configured to accept requests from multiple origins including:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

### Fixed Components

- **SigninForm Component**: Fixed redirect issue by moving from render-time redirect to useEffect hook to prevent React rendering errors
- **CORS Settings**: Updated to support multiple frontend ports (3000 and 3001)

## License

MIT
