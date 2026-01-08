# Quickstart Guide: Multi-User Todo Web Application

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and secrets
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL and other configurations
```

### 4. Database Setup

```bash
# From backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run database migrations
python -m alembic upgrade head

# Or create initial tables if using raw SQL
python -c "from src.database.database import engine; from src.models.user import User; from src.models.task import Task; User.metadata.create_all(engine); Task.metadata.create_all(engine)"
```

### 5. Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-32-character-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-32-character-secret-key-here
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

### 1. Start Backend Server

```bash
# From backend directory
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend Server

```bash
# From frontend directory
cd frontend
npm run dev
```

### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

## Basic Usage

### User Registration
1. Visit http://localhost:3000
2. Click "Sign Up" or navigate to /signup
3. Enter email and password (minimum 8 characters)
4. Account is created and you'll be redirected to login

### User Login
1. Visit http://localhost:3000
2. Click "Login" or navigate to /signin
3. Enter registered email and password
4. You'll be redirected to the dashboard

### Managing Tasks
1. After login, you'll be on the dashboard
2. Use the form to create new tasks
3. Toggle task completion with the checkbox
4. Edit tasks using the edit button
5. Delete tasks using the delete button

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/signin` - Authenticate user
- `POST /api/auth/signout` - Logout user

### Tasks
- `GET /api/tasks` - Get current user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle completion status

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure PostgreSQL is running and credentials are correct
- **Port Conflicts**: Check if ports 8000 (backend) or 3000 (frontend) are already in use
- **Environment Variables**: Verify all required environment variables are set
- **Dependency Issues**: Reinstall dependencies if experiencing import errors

### Resetting the Application
1. Drop and recreate the database
2. Run migrations again
3. Restart both frontend and backend servers