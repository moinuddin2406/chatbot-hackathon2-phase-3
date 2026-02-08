from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from sqlalchemy import JSON


def uuid_generator():
    return str(uuid4())


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: str = Field(default_factory=uuid_generator, primary_key=True)
    user_id: str = Field(index=True)  # Add index for user_id
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=uuid_generator, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Add foreign key constraint and index for user_id
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=uuid_generator, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)  # Add index
    user_id: str = Field(index=True)  # Add index for user_id
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON)  # Optional JSON object containing tool calls
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, index=True)  # Add index for created_at

    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")