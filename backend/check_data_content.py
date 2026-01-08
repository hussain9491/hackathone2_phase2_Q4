#!/usr/bin/env python3
"""Check actual data content in Neon database tables"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_data_content():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("DATABASE_URL not found in environment")
        return

    # Clean the URL by removing SSL parameters for connection
    url_parts = DATABASE_URL.split('?')
    base_url = url_parts[0]
    clean_url = base_url.replace("postgresql://", "postgresql+asyncpg://")

    engine = create_async_engine(clean_url)

    try:
        async with engine.begin() as conn:
            print("[INFO] Successfully connected to Neon database!")

            # Check user table
            print("\n--- User Table ---")
            user_result = await conn.execute(text("SELECT COUNT(*) FROM user;"))
            user_count = user_result.scalar()
            print(f"Total users: {user_count}")

            if user_count > 0:
                user_details = await conn.execute(text("SELECT id, email, created_at FROM user LIMIT 5;"))
                print("Sample user records:")
                for row in user_details:
                    print(f"  ID: {row[0]}, Email: {row[1]}, Created: {row[2]}")
            else:
                print("No user records found.")

            # Check task table
            print(f"\n--- Task Table ---")
            task_result = await conn.execute(text("SELECT COUNT(*) FROM task;"))
            task_count = task_result.scalar()
            print(f"Total tasks: {task_count}")

            if task_count > 0:
                task_details = await conn.execute(text("""
                    SELECT id, user_id, title, completed, created_at
                    FROM task
                    ORDER BY created_at DESC
                    LIMIT 5;
                """))
                print("Sample task records:")
                for row in task_details:
                    print(f"  ID: {row[0]}, User_ID: {row[1]}, Title: {row[2]}, Completed: {row[3]}, Created: {row[4]}")
            else:
                print("No task records found.")

            # Check table structures
            print(f"\n--- Table Structures ---")
            user_structure = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user';"))
            print("User table columns:")
            for col in user_structure:
                print(f"  {col[0]}: {col[1]}")

            task_structure = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'task';"))
            print("Task table columns:")
            for col in task_structure:
                print(f"  {col[0]}: {col[1]}")

    except Exception as e:
        print(f"[ERROR] Failed to check data content: {e}")

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_data_content())