from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os

# Import all models to register them with SQLModel
from .models.task import Task
from .models.user import User
from .models.conversation import Conversation, Message

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and "postgresql" in DATABASE_URL:
    # Handle asyncpg-specific URL format and remove unsupported parameters
    async_db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    # Remove channel_binding parameter as it's not supported by asyncpg
    if "channel_binding" in async_db_url:
        # Split the URL to remove the unsupported parameter
        base_url, params_str = async_db_url.split('?', 1) if '?' in async_db_url else (async_db_url, '')
        params = [p for p in params_str.split('&') if p and not p.startswith('channel_binding=')]
        if params:
            async_db_url = f"{base_url}?{'&'.join(params)}"
        else:
            async_db_url = base_url
    # Create async engine for PostgreSQL
    engine = create_async_engine(
        async_db_url,
        echo=True,
        future=True
    )
else:
    # Fallback for development (using SQLite with aiosqlite)
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True,
        future=True
    )

# Create async session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with async_session_maker() as session:
        yield session
