from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# Task Schemas
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False


class TaskCreate(TaskBase):
    user_id: str


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class Task(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    user_id: str


class Conversation(ConversationBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Message Schemas
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


class MessageBase(BaseModel):
    conversation_id: str
    user_id: str
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[List[ToolCall]] = None


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Chat Request/Response Schemas
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1)


class ToolCallResult(BaseModel):
    name: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: Optional[List[ToolCallResult]] = None