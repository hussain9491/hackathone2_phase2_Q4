#!/usr/bin/env python3
"""
Test script for the chat functionality
"""
import asyncio
import os
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Add the src directory to the path so we can import modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot.simple_agent import SimpleTodoAgent
from src.services.task_service import TaskService
from src.models.user import User
from src.models.task import Task

async def test_chat_functionality():
    """Test the chat functionality"""
    print("Testing chat functionality...")

    # Set up database connection
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and "postgresql" in DATABASE_URL:
        engine = create_async_engine(
            DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        # Create a test user
        user = User(
            id="test-user-id",
            email="test@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Test the agent
        agent = SimpleTodoAgent(session, user.id)

        # Test various messages
        test_messages = [
            "Add a task to buy groceries",
            "Show me my tasks",
            "Complete task 1",
            "Tell me about weather today"
        ]

        for msg in test_messages:
            print(f"\nTesting message: '{msg}'")
            result = await agent.process_message(msg)
            print(f"Response: {result['response']}")
            print(f"Tool calls: {result['tool_calls']}")

    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_chat_functionality())