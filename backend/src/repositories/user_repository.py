from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Create a new user"""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await self.session.get(User, user_id)

    async def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        user = await self.get_by_email(email)
        return user is not None

    async def update(self, user: User) -> User:
        """Update user"""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
