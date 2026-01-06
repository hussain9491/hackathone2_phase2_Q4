from typing import Optional
from sqlmodel import Field, SQLModel, Column, Text, ForeignKey
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    updated_at: datetime = Field(default_factory=datetime.now)
