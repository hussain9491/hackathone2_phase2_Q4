"""
AI Agent for Todo Task Management
Uses MCP tools for all task operations as specified in the architecture
"""
import re
import os
from typing import Dict, Any, List, Optional
from ..services.task_service import TaskService
from sqlmodel.ext.asyncio.session import AsyncSession
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import json


class SimpleTodoAgent:
    def __init__(self, session: AsyncSession, user_id: str):
        self.session = session
        self.user_id = user_id
        self.task_service = TaskService(session)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    async def _call_gemini_api(self, message: str, conversation_history: List[dict] = None) -> str:
        """Call the Gemini API to process the message"""
        if not self.model:
            # Fallback to rule-based processing if API key is not available
            return None

        try:
            # Prepare the chat history for Gemini
            chat_history = []

            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history:
                    # Map roles to Gemini format
                    role = "user" if msg["role"] == "user" else "model"  # Gemini uses "model" for assistant
                    chat_history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

            # Start a chat session with history
            chat = self.model.start_chat(history=chat_history)

            # Send the current message with instruction to use tools
            prompt = f"""
            You are a helpful AI assistant for task management.
            You must interpret user intent and respond with instructions for MCP tools to perform task operations.

            Available tools:
            - add_task: Create a new task
            - list_tasks: List tasks with optional status filter
            - complete_task: Mark a task as complete
            - update_task: Update task title or description
            - delete_task: Delete a task

            Respond with a JSON format indicating which tool to call and with what parameters.
            Example: {{"tool": "add_task", "params": {{"title": "Buy groceries", "description": "Milk and eggs"}}}}

            User message: {message}
            """

            response = await chat.send_message_async(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.3,  # Lower temp for more consistent tool usage
                    max_output_tokens=300
                )
            )

            return response.text.strip()

        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            return None

    async def _execute_tool_call(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate tool based on the tool call"""
        # Add user_id to parameters if not present
        params = params.copy()
        params["user_id"] = self.user_id

        if tool_name == "add_task":
            from .mcp_server import add_task
            # Use the same session as the agent instead of creating new engine
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            # Extract parameters
            user_id = params.get("user_id")
            title = params.get("title", "")
            description = params.get("description")

            try:
                task = await task_service.create_task(user_id, title, description)
                await self.session.commit()

                return {
                    "task_id": task.id,
                    "status": "created",
                    "title": task.title,
                    "message": f"Task '{task.title}' has been added successfully"
                }
            except Exception as e:
                return {
                    "error": True,
                    "code": "CREATE_TASK_ERROR",
                    "message": str(e)
                }
        elif tool_name == "list_tasks":
            from .mcp_server import list_tasks
            # Use the same session as the agent instead of creating new engine
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            # Extract parameters
            user_id = params.get("user_id")
            status = params.get("status", "all")

            try:
                result = await task_service.list_tasks(user_id, limit=100, offset=0)
                tasks = result["tasks"]

                # Filter based on status if specified
                if status == "pending":
                    tasks = [t for t in tasks if not t.completed]
                elif status == "completed":
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
                    "count": len(task_list),
                    "status_filter": status,
                    "message": f"Found {len(task_list)} {status} tasks"
                }
            except Exception as e:
                return {
                    "error": True,
                    "code": "LIST_TASKS_ERROR",
                    "message": str(e)
                }
        elif tool_name == "complete_task":
            from .mcp_server import complete_task
            # Use the same session as the agent instead of creating new engine
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            # Extract parameters
            user_id = params.get("user_id")
            task_id = params.get("task_id")

            try:
                task = await task_service.toggle_task(task_id, user_id)
                await self.session.commit()

                return {
                    "task_id": task.id,
                    "status": "completed" if task.completed else "pending",
                    "title": task.title,
                    "message": f"Task '{task.title}' marked as {'completed' if task.completed else 'pending'}"
                }
            except Exception as e:
                return {
                    "error": True,
                    "code": "COMPLETE_TASK_ERROR",
                    "message": str(e)
                }
        elif tool_name == "update_task":
            from .mcp_server import update_task
            # Use the same session as the agent instead of creating new engine
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            # Extract parameters
            user_id = params.get("user_id")
            task_id = params.get("task_id")
            title = params.get("title")
            description = params.get("description")

            try:
                task = await task_service.update_task(task_id, user_id, title, description)
                await self.session.commit()

                return {
                    "task_id": task.id,
                    "status": "updated",
                    "title": task.title,
                    "message": f"Task '{task.title}' has been updated"
                }
            except Exception as e:
                return {
                    "error": True,
                    "code": "UPDATE_TASK_ERROR",
                    "message": str(e)
                }
        elif tool_name == "delete_task":
            from .mcp_server import delete_task
            # Use the same session as the agent instead of creating new engine
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            # Extract parameters
            user_id = params.get("user_id")
            task_id = params.get("task_id")

            try:
                success = await task_service.delete_task(task_id, user_id)
                await self.session.commit()

                if success:
                    return {
                        "task_id": task_id,
                        "status": "deleted",
                        "message": f"Task {task_id} has been deleted"
                    }
                else:
                    return {
                        "error": True,
                        "code": "TASK_NOT_FOUND",
                        "message": f"Task {task_id} not found"
                    }
            except Exception as e:
                return {
                    "error": True,
                    "code": "DELETE_TASK_ERROR",
                    "message": str(e)
                }
        else:
            return {
                "error": True,
                "code": "UNKNOWN_TOOL",
                "message": f"Unknown tool: {tool_name}"
            }

    async def process_message(self, message: str, conversation_history: List[dict] = None) -> Dict[str, Any]:
        """Process a natural language message and return appropriate response"""

        # First, try to use the Gemini API for intelligent processing
        ai_response = await self._call_gemini_api(message, conversation_history)

        if ai_response:
            try:
                # Try to parse the AI response as JSON tool call
                # Sometimes the AI may return JSON wrapped in markdown or with extra text
                import re
                json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)

                if json_match:
                    tool_call_json = json_match.group()
                    tool_call = json.loads(tool_call_json)

                    if "tool" in tool_call and "params" in tool_call:
                        # Execute the tool call
                        result = await self._execute_tool_call(tool_call["tool"], tool_call["params"])

                        # Format the response
                        if result.get("error"):
                            response_text = f"Sorry, I encountered an error: {result.get('message', 'Unknown error occurred')}"
                        else:
                            response_text = result.get("message", f"Operation completed successfully")

                        return {
                            "response": response_text,
                            "tool_calls": [{
                                "tool": tool_call["tool"],
                                "parameters": tool_call["params"],
                                "result": result
                            }],
                            "action_taken": not result.get("error", False)
                        }
                    else:
                        # If the response is not a proper tool call, treat as regular response
                        return {
                            "response": ai_response,
                            "tool_calls": [],
                            "action_taken": False
                        }
                else:
                    # If no JSON found, treat as regular response
                    return {
                        "response": ai_response,
                        "tool_calls": [],
                        "action_taken": False
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, treat as regular response
                return {
                    "response": ai_response,
                    "tool_calls": [],
                    "action_taken": False
                }
        else:
            # Fallback to rule-based processing if API is not available
            message_lower = message.lower().strip()

            # Determine intent from message
            if self._is_add_intent(message_lower):
                return await self._handle_add_task_fallback(message)
            elif self._is_list_intent(message_lower):
                return await self._handle_list_tasks_fallback(message)
            elif self._is_complete_intent(message_lower):
                return await self._handle_complete_task_fallback(message)
            elif self._is_delete_intent(message_lower):
                return await self._handle_delete_task_fallback(message)
            elif self._is_update_intent(message_lower):
                return await self._handle_update_task_fallback(message)
            else:
                # Default response for unrecognized intents
                return {
                    "response": f"I understood your message: '{message}'. I can help you manage your tasks. Try saying things like 'add a task', 'show my tasks', 'complete task 1', etc.",
                    "tool_calls": [],
                    "action_taken": False
                }

    def _is_add_intent(self, message: str) -> bool:
        """Check if message indicates adding a task"""
        add_patterns = [
            r'\b(add|create|make|remember to|need to|put in|include)\b',
            r'\b(task|todo|thing to do|item)\b'
        ]
        return any(re.search(pattern, message) for pattern in add_patterns)

    def _is_list_intent(self, message: str) -> bool:
        """Check if message indicates listing tasks"""
        list_patterns = [
            r'\b(show|list|display|see|view|what do i have|my tasks|pending|outstanding)\b',
            r'\b(tasks|todos|things to do|items)\b'
        ]
        return any(re.search(pattern, message) for pattern in list_patterns)

    def _is_complete_intent(self, message: str) -> bool:
        """Check if message indicates completing a task"""
        complete_patterns = [
            r'\b(complete|done|finish|finished|marked as done|check off|tick|accomplished)\b',
            r'\b(task|todo|#\d+|\d+)\b'
        ]
        return any(re.search(pattern, message) for pattern in complete_patterns)

    def _is_delete_intent(self, message: str) -> bool:
        """Check if message indicates deleting a task"""
        delete_patterns = [
            r'\b(delete|remove|cancel|eliminate|get rid of|trash)\b',
            r'\b(task|todo)\b'
        ]
        return any(re.search(pattern, message) for pattern in delete_patterns)

    def _is_update_intent(self, message: str) -> bool:
        """Check if message indicates updating a task"""
        update_patterns = [
            r'\b(update|change|modify|edit|rename|alter)\b',
            r'\b(task|todo)\b'
        ]
        return any(re.search(pattern, message) for pattern in update_patterns)

    async def _extract_task_title(self, message: str) -> str:
        """Extract task title from message"""
        original_message = message.lower().strip()

        # Define patterns for common task creation phrases - ordered from most specific to least
        # Most important: Match "need to [action]" where [action] is the actual task
        patterns = [
            # Match "need to [task]", "want to [task]", "i want to [task]", "i need to [task]"
            # These should extract just the action part after "to"
            r'(?:need to|i want to|i need to|want to)\s+(.+)',

            # Match "remember to [task]" - extract just the task after "to"
            r'remember to\s+(.+)',

            # Match "add task to [title]", "create task to [title]", etc.
            r'(?:add|create|make)\s+(?:a\s+)?(?:task|todo|thing to do|item)?\s+to\s+(.+)',

            # Match "add [title]", "create [title]", "make [title]", etc. - more general
            r'(?:add|create|make|put in|include)\s+(.+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, original_message)
            if match:
                extracted = match.group(1).strip()

                # Further clean up common words that might remain
                extracted = re.sub(r'^to\s+', '', extracted)  # Remove leading "to"
                extracted = re.sub(r'^a\s+', '', extracted)   # Remove leading "a"
                extracted = re.sub(r'^an\s+', '', extracted)  # Remove leading "an"

                return extracted or "Untitled task"

        # If no pattern matched, return the original message cleaned up
        # Remove common prefixes that indicate task creation
        cleaned = re.sub(r'\b(add|create|make|remember to|need to|want to|i want to|i need to|put in|include)\s+', '', original_message, 1)
        cleaned = re.sub(r'\b(task|todo|thing to do|item)\s*', '', cleaned, 1)

        return cleaned.strip() or "Untitled task"

    async def _extract_task_number(self, message: str) -> Optional[str]:
        """Extract task number from message"""
        # Look for patterns like "#1", "task 1", "number 1", etc.
        patterns = [
            r'#(\d+)',
            r'task\s+(\d+)',
            r'number\s+(\d+)',
            r'(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1)
        return None

    async def _handle_add_task_fallback(self, message: str) -> Dict[str, Any]:
        """Handle adding a new task using direct service calls"""
        title = await self._extract_task_title(message)
        if not title or title == "Untitled task":
            # Try to extract the meaningful part from the message
            title = message.split('.')[0].split(',')[0].strip()
            # Remove common phrases
            for phrase in ['add ', 'create ', 'remember to ', 'need to ', 'i want to ']:
                if title.lower().startswith(phrase):
                    title = title[len(phrase):].strip()

        if not title:
            return {
                "response": "I wasn't able to extract a task title from your message. Could you please specify what task you'd like to add?",
                "tool_calls": [],
                "action_taken": False
            }

        try:
            # Use the task service directly with the same session
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            task = await task_service.create_task(self.user_id, title, None)
            await self.session.commit()

            return {
                "response": f"Task '{task.title}' has been added successfully",
                "tool_calls": [{
                    "tool": "add_task",
                    "parameters": {"title": title},
                    "result": {"task_id": task.id, "status": "created", "title": task.title, "message": f"Task '{task.title}' has been added successfully"}
                }],
                "action_taken": True
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't add the task: {str(e)}",
                "tool_calls": [],
                "action_taken": False
            }

    async def _handle_list_tasks_fallback(self, message: str) -> Dict[str, Any]:
        """Handle listing tasks using direct service calls"""
        try:
            # Determine if user wants all, pending, or completed tasks
            status = "all"
            if "pending" in message.lower() or "incomplete" in message.lower():
                status = "pending"
            elif "completed" in message.lower() or "done" in message.lower():
                status = "completed"

            # Use the task service directly with the same session
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            result = await task_service.list_tasks(self.user_id, limit=100, offset=0)
            tasks = result["tasks"]

            # Filter based on status if specified
            if status == "pending":
                tasks = [t for t in tasks if not t.completed]
            elif status == "completed":
                tasks = [t for t in tasks if t.completed]

            if not tasks:
                if status == "all":
                    response = "You don't have any tasks yet. You can add a task by saying something like 'add buy groceries'."
                elif status == "pending":
                    response = "You don't have any pending tasks. Great job staying on top of things!"
                else:  # completed
                    response = "You don't have any completed tasks yet. Start by adding and completing some tasks!"
            else:
                task_list = []
                for task in tasks[:10]:  # Limit to first 10 tasks to avoid overwhelming response
                    status_str = "✓" if task.completed else "○"
                    task_list.append(f"{status_str} #{task.id}: {task.title}")

                if len(tasks) > 10:
                    response = f"Here are your {status} tasks:\n" + "\n".join(task_list) + f"\n\n(+{len(tasks) - 10} more tasks not shown)"
                else:
                    response = f"Here are your {status} tasks:\n" + "\n".join(task_list)

            return {
                "response": response,
                "tool_calls": [{
                    "tool": "list_tasks",
                    "parameters": {"status": status},
                    "result": {"task_count": len(tasks)}
                }],
                "action_taken": True
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't retrieve your tasks: {str(e)}",
                "tool_calls": [],
                "action_taken": False
            }

    async def _handle_complete_task_fallback(self, message: str) -> Dict[str, Any]:
        """Handle completing a task using direct service calls"""
        task_number = await self._extract_task_number(message)

        if not task_number:
            return {
                "response": "I couldn't identify which task to complete. Please specify the task number like 'complete task 3' or 'mark task #5 as done'.",
                "tool_calls": [],
                "action_taken": False
            }

        try:
            # Use the task service directly with the same session
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            task = await task_service.toggle_task(task_number, self.user_id)
            await self.session.commit()

            return {
                "response": f"Task #{task.id} '{task.title}' is now marked as {'completed' if task.completed else 'pending'}.",
                "tool_calls": [{
                    "tool": "complete_task",
                    "parameters": {"task_id": task_number},
                    "result": {
                        "task_id": task.id,
                        "status": "completed" if task.completed else "pending",
                        "title": task.title,
                        "message": f"Task '{task.title}' marked as {'completed' if task.completed else 'pending'}"
                    }
                }],
                "action_taken": True
            }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't complete that task: {str(e)}. Make sure the task exists and belongs to you.",
                "tool_calls": [],
                "action_taken": False
            }

    async def _handle_delete_task_fallback(self, message: str) -> Dict[str, Any]:
        """Handle deleting a task using direct service calls"""
        task_number = await self._extract_task_number(message)

        if not task_number:
            return {
                "response": "I couldn't identify which task to delete. Please specify the task number like 'delete task 3' or 'remove task #5'.",
                "tool_calls": [],
                "action_taken": False
            }

        try:
            # Use the task service directly with the same session
            from ..services.task_service import TaskService
            task_service = TaskService(self.session)

            success = await task_service.delete_task(task_number, self.user_id)
            await self.session.commit()

            if success:
                return {
                    "response": f"Task {task_number} has been deleted successfully.",
                    "tool_calls": [{
                        "tool": "delete_task",
                        "parameters": {"task_id": task_number},
                        "result": {
                            "task_id": task_number,
                            "status": "deleted",
                            "message": f"Task {task_number} has been deleted"
                        }
                    }],
                    "action_taken": True
                }
            else:
                return {
                    "response": f"Sorry, I couldn't find task #{task_number} to delete: Task not found",
                    "tool_calls": [],
                    "action_taken": False
                }
        except Exception as e:
            return {
                "response": f"Sorry, I couldn't delete that task: {str(e)}. Make sure the task exists and belongs to you.",
                "tool_calls": [],
                "action_taken": False
            }

    async def _handle_update_task_fallback(self, message: str) -> Dict[str, Any]:
        """Handle updating a task - this is more complex, just return a helpful message"""
        return {
            "response": f"I understand you want to update a task. For now, I recommend using the dashboard UI to edit tasks. In the future, you'll be able to say something like 'update task 3 to buy milk instead'.",
            "tool_calls": [],
            "action_taken": False
        }