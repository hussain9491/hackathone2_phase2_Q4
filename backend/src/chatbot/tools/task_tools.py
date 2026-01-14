"""
MCP Tools for Todo Task Management
Following MCP Protocol Standards from CLAUDE.md
"""
import asyncio
from typing import Optional, Dict, Any, List
from mcp import server, types
from mcp.server import jsonrpc
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..models.task import Task
from ..services.task_service import TaskService
import os
import json

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and "postgresql" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    )
else:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksRequest(BaseModel):
    user_id: str
    status: Optional[str] = "all"  # "all", "pending", "completed"


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


async def add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool to add a new task"""
    request = AddTaskRequest(**params)

    async with async_session_maker() as session:
        task_service = TaskService(session)
        task = await task_service.create_task(
            user_id=request.user_id,
            title=request.title,
            description=request.description
        )

        await session.commit()

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "message": f"Task '{task.title}' has been added successfully"
        }


async def list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool to list tasks"""
    request = ListTasksRequest(**params)

    async with async_session_maker() as session:
        task_service = TaskService(session)
        result = await task_service.list_tasks(request.user_id, limit=100, offset=0)

        tasks = result["tasks"]

        # Filter based on status if specified
        if request.status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif request.status == "completed":
            tasks = [t for t in tasks if t.completed]

        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            })

        return {
            "tasks": task_list,
            "total": len(task_list),
            "status": request.status,
            "message": f"Found {len(task_list)} {request.status} tasks"
        }


async def complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool to complete a task"""
    request = CompleteTaskRequest(**params)

    async with async_session_maker() as session:
        task_service = TaskService(session)
        task = await task_service.toggle_task(request.task_id, request.user_id)

        await session.commit()

        return {
            "task_id": task.id,
            "status": "completed" if task.completed else "pending",
            "title": task.title,
            "message": f"Task '{task.title}' marked as {'completed' if task.completed else 'pending'}"
        }


async def update_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool to update a task"""
    request = UpdateTaskRequest(**params)

    async with async_session_maker() as session:
        task_service = TaskService(session)
        task = await task_service.update_task(
            request.task_id,
            request.user_id,
            request.title,
            request.description
        )

        await session.commit()

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "message": f"Task '{task.title}' has been updated"
        }


async def delete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool to delete a task"""
    request = DeleteTaskRequest(**params)

    async with async_session_maker() as session:
        task_service = TaskService(session)
        success = await task_service.delete_task(request.task_id, request.user_id)

        await session.commit()

        if success:
            return {
                "task_id": request.task_id,
                "status": "deleted",
                "message": f"Task {request.task_id} has been deleted"
            }
        else:
            return {
                "error": True,
                "code": "TASK_NOT_FOUND",
                "message": f"Task {request.task_id} not found"
            }


def create_mcp_server() -> server.Server:
    """Create and configure the MCP server with all task tools"""
    svr = server.Server("todo-task-agent")

    @svr.tool("add_task")
    async def add_task_tool(context, params: types.ToolCallRequest) -> types.ToolResult:
        try:
            result = await add_task(params)
            return types.ToolResult(content=json.dumps(result), is_error=False)
        except Exception as e:
            error_result = {
                "error": True,
                "code": "INVALID_INPUT",
                "message": str(e)
            }
            return types.ToolResult(content=json.dumps(error_result), is_error=True)

    @svr.tool("list_tasks")
    async def list_tasks_tool(context, params: types.ToolCallRequest) -> types.ToolResult:
        try:
            result = await list_tasks(params)
            return types.ToolResult(content=json.dumps(result), is_error=False)
        except Exception as e:
            error_result = {
                "error": True,
                "code": "INVALID_INPUT",
                "message": str(e)
            }
            return types.ToolResult(content=json.dumps(error_result), is_error=True)

    @svr.tool("complete_task")
    async def complete_task_tool(context, params: types.ToolCallRequest) -> types.ToolResult:
        try:
            result = await complete_task(params)
            return types.ToolResult(content=json.dumps(result), is_error=False)
        except Exception as e:
            error_result = {
                "error": True,
                "code": "INVALID_INPUT",
                "message": str(e)
            }
            return types.ToolResult(content=json.dumps(error_result), is_error=True)

    @svr.tool("update_task")
    async def update_task_tool(context, params: types.ToolCallRequest) -> types.ToolResult:
        try:
            result = await update_task(params)
            return types.ToolResult(content=json.dumps(result), is_error=False)
        except Exception as e:
            error_result = {
                "error": True,
                "code": "INVALID_INPUT",
                "message": str(e)
            }
            return types.ToolResult(content=json.dumps(error_result), is_error=True)

    @svr.tool("delete_task")
    async def delete_task_tool(context, params: types.ToolCallRequest) -> types.ToolResult:
        try:
            result = await delete_task(params)
            return types.ToolResult(content=json.dumps(result), is_error=False)
        except Exception as e:
            error_result = {
                "error": True,
                "code": "INVALID_INPUT",
                "message": str(e)
            }
            return types.ToolResult(content=json.dumps(error_result), is_error=True)

    return svr