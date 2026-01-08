from fastapi import APIRouter, Depends, HTTPException, status, Query, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.task_service import TaskService
from ..dependencies import get_db_session
from ..auth import decode_access_token
import os

# Security scheme for Swagger UI
security = HTTPBearer(scheme_name="Bearer")

router = APIRouter(tags=["tasks"])

# Request/Response models
class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    limit: int
    offset: int

class ErrorResponse(BaseModel):
    error: str

def get_current_user_id( credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Extract user_id from JWT token using HTTPBearer security"""
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload.get("sub")

@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """List all tasks for user"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    task_service = TaskService(session)
    result = await task_service.list_tasks(user_id, limit, offset)

    # Convert Task objects to dictionaries with string-formatted dates
    formatted_tasks = []
    for task in result["tasks"]:
        formatted_tasks.append({
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })

    return {
        "tasks": formatted_tasks,
        "total": result["total"],
        "limit": result["limit"],
        "offset": result["offset"]
    }

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    request: CreateTaskRequest,
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """Create new task"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create task for different user"
        )

    task_service = TaskService(session)
    task = await task_service.create_task(auth_user_id, request.title, request.description)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """Get single task"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    task_service = TaskService(session)
    task = await task_service.get_task(task_id, user_id)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    request: UpdateTaskRequest,
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """Update task"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update task for different user"
        )

    task_service = TaskService(session)
    task = await task_service.update_task(task_id, user_id, request.title, request.description)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """Delete task"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete task for different user"
        )

    task_service = TaskService(session)
    success = await task_service.delete_task(task_id, user_id)
    if success:
        return {"message": "Task deleted successfully"}
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_db_session),
    auth_user_id: str = Depends(get_current_user_id),
):
    """Toggle task completion status"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot toggle task for different user"
        )

    task_service = TaskService(session)
    task = await task_service.toggle_task(task_id, user_id)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )
