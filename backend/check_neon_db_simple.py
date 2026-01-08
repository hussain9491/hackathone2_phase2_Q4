#!/usr/bin/env python3
"""Script to check Neon database connectivity using the same approach as the main app"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime

# Import your models
from src.models.user import User
from src.models.task import Task

async def check_database():
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set!")
        return

    print(f"Connecting to database: {DATABASE_URL.replace('@', '***@')[:50]}...")

    # Use the same approach as in database.py
    if DATABASE_URL and "postgresql" in DATABASE_URL:
        # Create async engine for PostgreSQL (same as in database.py)
        engine = create_async_engine(
            DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=True,
        )
    else:
        print("ERROR: Not a PostgreSQL URL")
        return

    # Create async session factory
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    try:
        # First, let's just try to connect and get table information
        print("\n--- Testing Connection ---")
        async with engine.begin() as conn:
            print("✓ Successfully connected to database")

            # Check if tables exist by executing a simple query
            from sqlalchemy import text
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"Tables in database: {tables}")

            # Check if our expected tables exist
            expected_tables = ['user', 'task']
            for table in expected_tables:
                if table in tables:
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' does not exist")

        # Now check the actual data in the tables
        async with async_session_maker() as session:
            print("\n--- Checking User Table ---")
            try:
                # Count users
                result = await session.execute(select(User))
                users = result.scalars().all()
                print(f"Total users: {len(users)}")

                # Display user information (without sensitive data)
                for i, user in enumerate(users):
                    print(f"User {i+1}: ID={user.id}, Email={user.email}, Created={user.created_at}")

            except Exception as e:
                print(f"Error querying users: {e}")

            print("\n--- Checking Task Table ---")
            try:
                # Count tasks
                result = await session.execute(select(Task))
                tasks = result.scalars().all()
                print(f"Total tasks: {len(tasks)}")

                # Display task information
                for i, task in enumerate(tasks):
                    print(f"Task {i+1}: ID={task.id}, Title='{task.title}', Completed={task.completed}, User_ID={task.user_id}, Created={task.created_at}")

            except Exception as e:
                print(f"Error querying tasks: {e}")

        print("\n✓ Database check completed successfully!")

    except Exception as e:
        print(f"Database connection error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the engine
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_database())