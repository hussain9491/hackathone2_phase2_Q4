from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and "postgresql" in DATABASE_URL:
    # Create async engine for PostgreSQL
    engine = create_async_engine(
        DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
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
