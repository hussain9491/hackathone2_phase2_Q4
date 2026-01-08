#!/usr/bin/env python3
"""Check actual schema and table information in Neon database"""

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_schema_info():
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

            # Check all schemas
            print("\n--- All Schemas ---")
            schemas = await conn.execute(text("SELECT schema_name FROM information_schema.schemata;"))
            schema_list = [row[0] for row in schemas]
            print(f"Schemas: {schema_list}")

            # Check tables in all schemas
            print("\n--- Tables in All Schemas ---")
            all_tables = await conn.execute(text("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                ORDER BY table_schema, table_name;
            """))

            tables_by_schema = {}
            for row in all_tables:
                schema, table_name = row[0], row[1]
                if schema not in tables_by_schema:
                    tables_by_schema[schema] = []
                tables_by_schema[schema].append(table_name)

            for schema, tables in tables_by_schema.items():
                print(f"Schema '{schema}': {tables}")

            # Specifically check public schema
            print(f"\n--- Checking 'public' Schema Tables ---")
            public_tables = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """))
            public_table_names = [row[0] for row in public_tables]
            print(f"Tables in 'public' schema: {public_table_names}")

            # Try to query the actual tables in the public schema
            for table_name in public_table_names:
                print(f"\n--- Data in '{table_name}' table ---")
                try:
                    count_result = await conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name};"))
                    count = count_result.scalar()
                    print(f"Total records: {count}")

                    if count > 0:
                        # Get first few records
                        sample_result = await conn.execute(text(f"SELECT * FROM public.{table_name} LIMIT 3;"))
                        print("Sample records:")
                        for i, row in enumerate(sample_result):
                            print(f"  Record {i+1}: {dict(row._mapping)}")

                except Exception as e:
                    print(f"Error querying {table_name}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to check schema info: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_schema_info())