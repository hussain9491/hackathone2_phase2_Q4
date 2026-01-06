from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(index=True, max_length=255, unique=True)
    password_hash: str = Field(max_length=255)

class User(UserBase, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
