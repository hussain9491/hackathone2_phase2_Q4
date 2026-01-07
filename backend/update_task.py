#!/usr/bin/env python3
"""
Script to update a task in the NeonDB database.
This script will:
1. Connect to the database
2. Find an existing task (or create one if needed)
3. Update the task with new information
4. Verify the update was successful
"""

import asyncio
import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is not required

# Import models and services
from src.models.task import Task
from src.models.user import User
from src.services.user_service import UserService
from src.services.task_service import TaskService


async def update_task_in_database():
    """Update a task in the database"""

    # Database URL from environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL and "postgresql" in DATABASE_URL:
        # Handle NeonDB connection string with SSL parameters
        db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

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

    print("Updating task in NeonDB...")

    async with engine.begin() as conn:
        # Initialize database tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        # Create or find a user to associate with the task
        user_service = UserService(session)

        # Try to find an existing user or create a test user
        test_email = f"test_update_user_{int(datetime.now().timestamp())}@example.com"
        test_password = "password123"

        print(f"Creating test user: {test_email}")
        try:
            user_data = await user_service.create_user(test_email, test_password)
            if user_data and 'id' in user_data:
                user_id = user_data['id']
                print(f"OK User created with ID: {user_id}")
            else:
                print("X Error creating user: Invalid response from create_user")
                return False
        except Exception as e:
            print(f"X Error creating user: {e}")
            return False

        # Create a task to update
        task_service = TaskService(session)

        original_title = "Original Task Title"
        original_description = "This is the original task description"

        print(f"Creating task to update: {original_title}")
        try:
            original_task = await task_service.create_task(
                user_id=user_id,
                title=original_title,
                description=original_description
            )
            print(f"OK Task created with ID: {original_task.id}")
        except Exception as e:
            print(f"X Error creating task: {e}")
            return False

        # Now update the task
        updated_title = "Updated Task Title"
        updated_description = "This is the updated task description with new information"

        print(f"Updating task with ID: {original_task.id}")
        print(f"  New title: {updated_title}")
        print(f"  New description: {updated_description}")

        try:
            updated_task = await task_service.update_task(
                task_id=original_task.id,
                user_id=user_id,
                title=updated_title,
                description=updated_description
            )

            if updated_task:
                print(f"OK Task updated successfully!")
                print(f"  - ID: {updated_task.id}")
                print(f"  - Title: {updated_task.title}")
                print(f"  - Description: {updated_task.description}")
                print(f"  - Completed: {updated_task.completed}")
                print(f"  - Updated at: {updated_task.updated_at}")

                # Verify the task was actually updated in the database
                retrieved_task = await session.get(Task, original_task.id)
                if retrieved_task and retrieved_task.title == updated_title and retrieved_task.description == updated_description:
                    print("OK Task update verified in database!")
                    return True
                else:
                    print("X Task update not found in database after update")
                    return False
            else:
                print("X Failed to update task")
                return False

        except Exception as e:
            print(f"X Error updating task: {e}")
            return False


if __name__ == "__main__":
    success = asyncio.run(update_task_in_database())
    if success:
        print("\nSUCCESS Task update completed successfully!")
        print("Task was properly updated in NeonDB.")
    else:
        print("\nFAILED Task update failed!")
        exit(1)