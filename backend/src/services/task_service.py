from typing import Optional, List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..repositories.task_repository import TaskRepository
from ..models.task import Task, TaskBase

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.task_repo = TaskRepository(session)

    async def validate_task_limit(self, user_id: str) -> bool:
        """Check if user has reached maximum task limit (1000)"""
        count = await self.task_repo.count_by_user(user_id)
        return count < 1000

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Optional[Task]:
        """Create a new task for user"""
        # Validate title length
        if len(title) < 1 or len(title) > 200:
            raise ValueError("Title must be 1-200 characters")

        # Validate description length
        if description and len(description) > 1000:
            raise ValueError("Description must be under 1000 characters")

        # Check task limit
        if not await self.validate_task_limit(user_id):
            raise ValueError("Maximum task limit reached (1000 tasks per user)")

        # Create task
        task = Task(user_id=user_id, title=title, description=description)
        return await self.task_repo.create(task)

    async def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get task with ownership verification"""
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.user_id != user_id:
            raise ValueError("Task not found")
        return task

    async def list_tasks(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List tasks for user with pagination"""
        tasks = await self.task_repo.list_by_user(user_id, limit, offset)
        total = await self.task_repo.count_by_user(user_id)
        return {
            "tasks": tasks,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    async def update_task(
        self,
        task_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Task]:
        """Update task with ownership verification"""
        task = await self.get_task(task_id, user_id)

        # Update fields if provided
        if title is not None:
            if len(title) < 1 or len(title) > 200:
                raise ValueError("Title must be 1-200 characters")
            task.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description must be under 1000 characters")
            task.description = description

        return await self.task_repo.update(task)

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete task with ownership verification"""
        task = await self.get_task(task_id, user_id)
        return await self.task_repo.delete(task_id)

    async def toggle_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Toggle task completion status with ownership verification"""
        task = await self.get_task(task_id, user_id)
        return await self.task_repo.toggle_complete(task_id)
