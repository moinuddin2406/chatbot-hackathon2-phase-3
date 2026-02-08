from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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


class TaskResponse(BaseModel):
    success: bool
    data: Optional[Task] = None
    error: Optional[dict] = None