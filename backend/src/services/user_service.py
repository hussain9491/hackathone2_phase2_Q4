import re
from typing import Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..repositories.user_repository import UserRepository
from ..models.user import User, UserBase
from ..auth import hash_password, verify_password, create_access_token

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        return re.match(EMAIL_REGEX, email) is not None

    def validate_password(self, password: str) -> bool:
        """Validate password (minimum 8 characters)"""
        return len(password) >= 8

    async def create_user(
        self,
        email: str,
        password: str
    ) -> Optional[User]:
        """Create a new user with hashed password"""
        # Validate email format
        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        # Validate password length
        if not self.validate_password(password):
            raise ValueError("Password must be at least 8 characters")

        # Check email uniqueness
        if await self.user_repo.email_exists(email):
            raise ValueError("Email already registered")

        # Hash password and create user
        password_hash = hash_password(password)
        from datetime import datetime
        user = User(
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        created_user = await self.user_repo.create(user)

        # Create JWT token for the newly created user
        token_data = {
            "sub": created_user.id,
            "email": created_user.email
        }
        access_token = create_access_token(token_data)

        # Return properly formatted response
        return {
            "id": created_user.id,
            "email": created_user.email,
            "token": access_token,
            "created_at": created_user.created_at.isoformat(),
            "updated_at": created_user.updated_at.isoformat()
        }

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[Dict[str, Any]]:
        """Authenticate user and return access token"""
        # Validate email format
        if not self.validate_email(email):
            raise ValueError("Invalid email format")

        # Find user by email
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Update last login time
        from datetime import datetime
        user.updated_at = datetime.now()
        await self.user_repo.update(user)

        # Create JWT token
        token_data = {
            "sub": user.id,
            "email": user.email
        }
        access_token = create_access_token(token_data)

        return {
            "id": user.id,
            "email": user.email,
            "token": access_token,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
