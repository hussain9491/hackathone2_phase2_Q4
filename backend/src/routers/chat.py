"""
Chat endpoint for the Todo AI Chatbot
Handles natural language interactions and MCP tool integration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from ..auth import decode_access_token
from ..services.chat_service import ConversationService
from ..dependencies import get_db_session
from ..chatbot.simple_agent import SimpleTodoAgent
import os

router = APIRouter(tags=["chat"])

# Security scheme for Swagger UI
security = HTTPBearer(scheme_name="Bearer")

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user_id from JWT token using HTTPBearer security"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload.get("sub")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    auth_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """Chat endpoint that processes natural language and uses task tools"""
    # Verify user_id matches token
    if auth_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access chat for different user"
        )

    chat_service = ConversationService(session)

    # Get or create conversation
    if request.conversation_id:
        conversation = await chat_service.get_conversation(request.conversation_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        conversation_id = request.conversation_id
    else:
        conversation = await chat_service.create_conversation(user_id)
        conversation_id = conversation.id

    # Add user message to conversation
    await chat_service.add_message(conversation_id, user_id, "user", request.message)

    # Get conversation history for context
    all_messages = await chat_service.get_messages(conversation_id, user_id)

    # Prepare message history for the agent
    conversation_history = []
    for msg in all_messages:
        conversation_history.append({
            "role": msg.role,
            "content": msg.content
        })

    # Process the message with the simple AI agent
    agent = SimpleTodoAgent(session, user_id)
    result = await agent.process_message(request.message, conversation_history)

    response_text = result["response"]
    tool_calls = result.get("tool_calls", [])

    # Add assistant response to conversation
    await chat_service.add_message(
        conversation_id,
        user_id,
        "assistant",
        response_text,
        str(tool_calls) if tool_calls else None
    )

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=tool_calls
    )