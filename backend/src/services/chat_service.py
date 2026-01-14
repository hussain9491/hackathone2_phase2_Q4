from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.conversation import Conversation, Message
from datetime import datetime


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: str) -> Conversation:
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: int, user_id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_messages(self, conversation_id: int, user_id: str) -> List[Message]:
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at.asc())
        result = await self.session.exec(statement)
        return result.all()

    async def add_message(self, conversation_id: int, user_id: str, role: str, content: str, tool_calls: Optional[str] = None) -> Message:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message