#!/usr/bin/env python3
"""Script to check Neon database connectivity and verify data storage"""

import asyncio
import os
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime

# Import your models
from src.models.user import User
from src.models.task import Task

async def check_database():
    # Try to load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv is optional

    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set!")
        return

    print(f"Connecting to database: {DATABASE_URL.replace('@', '***@')[:50]}...")

    # Handle the SSL parameters that might cause issues with asyncpg
    # We'll try to connect with the original URL but handle the SSL params appropriately
    db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    # Create async engine for PostgreSQL
    engine = create_async_engine(
        db_url,
        echo=True,
    )

    # Create async session factory
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    try:
        # Test connection by getting table information
        async with engine.begin() as conn:
            # Check if tables exist by reflecting metadata
            from sqlalchemy import inspect
            from sqlalchemy.dialects import postgresql

            # Get table names
            result = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            print(f"\nTables in database: {result}")

            # Check if our expected tables exist
            expected_tables = ['user', 'task']
            for table in expected_tables:
                if table in result:
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' does not exist")

        # Now check the actual data in the tables
        async with async_session_maker() as session:
            print("\n--- Checking User Table ---")
            try:
                # Count users
                user_count = await session.exec(select(User))
                users = user_count.all()
                print(f"Total users: {len(users)}")

                # Display user information (without sensitive data)
                for i, user in enumerate(users):
                    print(f"User {i+1}: ID={user.id}, Email={user.email}, Created={user.created_at}")

            except Exception as e:
                print(f"Error querying users: {e}")

            print("\n--- Checking Task Table ---")
            try:
                # Count tasks
                task_count = await session.exec(select(Task))
                tasks = task_count.all()
                print(f"Total tasks: {len(tasks)}")

                # Display task information
                for i, task in enumerate(tasks):
                    print(f"Task {i+1}: ID={task.id}, Title='{task.title}', Completed={task.completed}, User_ID={task.user_id}, Created={task.created_at}")

            except Exception as e:
                print(f"Error querying tasks: {e}")

    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        # Close the engine
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_database())