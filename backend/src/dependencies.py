from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import async_session_maker
from fastapi import Depends

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Type alias for dependency injection
SessionDep = AsyncSession
