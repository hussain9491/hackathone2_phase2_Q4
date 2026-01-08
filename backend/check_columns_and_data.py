#!/usr/bin/env python3
"""Check actual column names and data in Neon database tables"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_columns_and_data():
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

            # Check actual column names in user table
            print("\n--- User Table Columns ---")
            user_cols = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'user'
                ORDER BY ordinal_position;
            """))

            user_columns = []
            print("User table schema:")
            for col in user_cols:
                col_name = col[0]
                user_columns.append(col_name)
                print(f"  {col_name}: {col[1]} (nullable: {col[2]}, default: {col[3]})")

            # Check actual column names in task table
            print("\n--- Task Table Columns ---")
            task_cols = await conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'task'
                ORDER BY ordinal_position;
            """))

            task_columns = []
            print("Task table schema:")
            for col in task_cols:
                col_name = col[0]
                task_columns.append(col_name)
                print(f"  {col_name}: {col[1]} (nullable: {col[2]}, default: {col[3]})")

            # Check user table data with correct column names
            print(f"\n--- User Table Data ---")
            user_result = await conn.execute(text("SELECT COUNT(*) FROM user;"))
            user_count = user_result.scalar()
            print(f"Total users: {user_count}")

            if user_count > 0:
                # Build dynamic query based on actual columns
                user_col_list = ', '.join(user_columns)
                user_query = f"SELECT {user_col_list} FROM user LIMIT 5;"

                user_details = await conn.execute(text(user_query))
                print("Sample user records:")
                for row in user_details:
                    print(f"  Row data: {dict(row._mapping)}")
            else:
                print("No user records found.")

            # Check task table data with correct column names
            print(f"\n--- Task Table Data ---")
            task_result = await conn.execute(text("SELECT COUNT(*) FROM task;"))
            task_count = task_result.scalar()
            print(f"Total tasks: {task_count}")

            if task_count > 0:
                # Build dynamic query based on actual columns
                task_col_list = ', '.join(task_columns)
                task_query = f"SELECT {task_col_list} FROM task ORDER BY created_at DESC LIMIT 5;"

                task_details = await conn.execute(text(task_query))
                print("Sample task records:")
                for row in task_details:
                    print(f"  Row data: {dict(row._mapping)}")
            else:
                print("No task records found.")

    except Exception as e:
        print(f"[ERROR] Failed to check data content: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_columns_and_data())