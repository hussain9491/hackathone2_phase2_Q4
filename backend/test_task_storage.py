#!/usr/bin/env python3
"""
Test script to verify that tasks are being saved to NeonDB.
This script will:
1. Create a test user
2. Create a task for that user
3. Verify the task exists in the database
"""

import asyncio
import os
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is not required

# Import models
from src.models.user import User
from src.models.task import Task
from src.services.user_service import UserService
from src.services.task_service import TaskService


async def test_task_storage():
    """Test that tasks are properly stored in the database"""

    # Database URL from environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL and "postgresql" in DATABASE_URL:
        # Handle NeonDB connection string with SSL parameters
        # Remove SSL parameters that asyncpg doesn't support directly
        db_url = DATABASE_URL

        # Replace postgresql:// with postgresql+asyncpg:// and remove SSL parameters
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

        # Remove SSL-related parameters that asyncpg doesn't support
        import urllib.parse
        parsed = urllib.parse.urlparse(db_url)

        # Rebuild URL without SSL parameters
        query_params = urllib.parse.parse_qs(parsed.query)
        # Remove problematic parameters
        for param in ['sslmode', 'channel_binding', 'options']:
            query_params.pop(param, None)

        # Reconstruct query string without SSL params
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        db_url = urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))

        # Create async engine for PostgreSQL
        engine = create_async_engine(
            db_url,
            echo=True,
            future=True
        )
    else:
        print("ERROR: DATABASE_URL not found or not a PostgreSQL URL")
        return False

    # Create async session factory
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    print("Testing task storage in NeonDB...")

    # Initialize database tables if they don't exist
    async with engine.begin() as conn:
        from src.database import SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        # Create a test user
        user_service = UserService(session)

        test_email = f"test_user_{int(datetime.now().timestamp())}@example.com"
        test_password = "password123"

        print(f"Creating test user: {test_email}")
        try:
            user_data = await user_service.create_user(test_email, test_password)
            if user_data and 'id' in user_data:
                print(f"OK User created with ID: {user_data['id']}")
                user_id = user_data['id']
            else:
                print("X Error creating user: Invalid response from create_user")
                return False
        except Exception as e:
            print(f"X Error creating user: {e}")
            return False

        # Create a task for the user
        task_service = TaskService(session)

        task_title = "Test task for NeonDB verification"
        task_description = "This task verifies that data is properly stored in NeonDB"

        print(f"Creating task: {task_title}")
        try:
            task = await task_service.create_task(
                user_id=user_id,
                title=task_title,
                description=task_description
            )
            print(f"OK Task created with ID: {task.id}")
        except Exception as e:
            print(f"X Error creating task: {e}")
            return False

        # Verify the task exists in the database
        print("Verifying task exists in database...")
        try:
            retrieved_task = await session.get(Task, task.id)
            if retrieved_task:
                print(f"OK Task found in database: {retrieved_task.title}")
                print(f"  - ID: {retrieved_task.id}")
                print(f"  - User ID: {retrieved_task.user_id}")
                print(f"  - Title: {retrieved_task.title}")
                print(f"  - Description: {retrieved_task.description}")
                print(f"  - Completed: {retrieved_task.completed}")
                print(f"  - Created at: {retrieved_task.created_at}")

                # Verify it's the same user
                if retrieved_task.user_id == user_id:
                    print("OK Task is correctly associated with the user")
                else:
                    print("X Task user ID doesn't match")
                    return False
            else:
                print("X Task not found in database")
                return False
        except Exception as e:
            print(f"X Error retrieving task: {e}")
            return False

        # Test listing tasks for the user
        print("Testing task listing...")
        try:
            task_list_result = await task_service.list_tasks(user_id)
            tasks = task_list_result["tasks"]
            total = task_list_result["total"]

            print(f"OK Found {total} task(s) for user")
            if total > 0:
                found_task = False
                for t in tasks:
                    if t.id == task.id:
                        found_task = True
                        print(f"  - Found task in user's list: {t.title}")
                        break

                if not found_task:
                    print("X Created task not found in user's task list")
                    return False
            else:
                print("X No tasks found for user")
                return False
        except Exception as e:
            print(f"X Error listing tasks: {e}")
            return False

        print("\nOK All tests passed! Tasks are being properly saved to NeonDB")
        return True


if __name__ == "__main__":
    success = asyncio.run(test_task_storage())
    if success:
        print("\nSUCCESS Task storage test completed successfully!")
        print("Tasks are being properly saved to NeonDB.")
    else:
        print("\nFAILED Task storage test failed!")
        exit(1)