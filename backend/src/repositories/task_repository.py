from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.task import Task

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        """Create a new task"""
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return await self.session.get(Task, task_id)

    async def list_by_user(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """List all tasks for a user, ordered by created_at DESC"""
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.completed, Task.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def count_by_user(self, user_id: str) -> int:
        """Count total tasks for a user"""
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        return len(list(result.scalars().all()))

    async def update(self, task: Task) -> Task:
        """Update task"""
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: str) -> bool:
        """Delete task by ID"""
        task = await self.get_by_id(task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        return False

    async def toggle_complete(self, task_id: str) -> Optional[Task]:
        """Toggle task completion status"""
        task = await self.get_by_id(task_id)
        if task:
            task.completed = not task.completed
            await self.session.commit()
            await self.session.refresh(task)
            return task
        return None
