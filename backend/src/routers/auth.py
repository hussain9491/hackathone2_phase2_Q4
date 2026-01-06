from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.user_service import UserService
from ..dependencies import get_db_session

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Request models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

# Response models
class AuthResponse(BaseModel):
    id: str
    email: str
    token: str
    created_at: str
    updated_at: str

class ErrorResponse(BaseModel):
    error: str

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: AsyncSession = Depends(get_db_session)
):
    """Create new user account"""
    try:
        user_service = UserService(session)
        result = await user_service.create_user(request.email, request.password)
        return result
    except ValueError as e:
        if "Invalid email format" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        elif "Password must be" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )
        elif "Email already registered" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SigninRequest,
    session: AsyncSession = Depends(get_db_session)
):
    """Sign in existing user"""
    try:
        user_service = UserService(session)
        result = await user_service.authenticate_user(request.email, request.password)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
