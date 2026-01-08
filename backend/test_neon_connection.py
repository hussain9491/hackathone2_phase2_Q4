#!/usr/bin/env python3
"""Simple test to check Neon database connection"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("DATABASE_URL not found in environment")
        return

    print(f"Original URL: {DATABASE_URL[:50]}...")

    # Try to remove problematic parameters
    url_parts = DATABASE_URL.split('?')
    base_url = url_parts[0]

    # Extract parameters
    if len(url_parts) > 1:
        params = url_parts[1]
        print(f"Parameters: {params}")

        # Try without SSL parameters
        clean_url = f"{base_url}"
    else:
        clean_url = DATABASE_URL

    # Convert to asyncpg format
    clean_url = clean_url.replace("postgresql://", "postgresql+asyncpg://")

    print(f"Testing connection with: {clean_url[:50]}...")

    # Create engine without SSL parameters
    engine = create_async_engine(clean_url)

    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"[SUCCESS] Connected successfully! Database version: {version}")

            # Check for tables
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = [row[0] for row in result]
            print(f"Tables found: {tables}")

            return True
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

        # Try with SSL disabled
        ssl_disabled_url = f"{clean_url}?sslmode=disable"
        print(f"Trying with SSL disabled: {ssl_disabled_url[:50]}...")

        try:
            engine_ssl = create_async_engine(ssl_disabled_url)
            async with engine_ssl.begin() as conn:
                result = await conn.execute(text("SELECT version();"))
                version = result.scalar()
                print(f"[SUCCESS] Connected with SSL disabled! Database version: {version}")

                # Check for tables
                result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
                tables = [row[0] for row in result]
                print(f"Tables found: {tables}")

                return True
        except Exception as e2:
            print(f"[ERROR] Connection with SSL disabled also failed: {e2}")
            return False
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())