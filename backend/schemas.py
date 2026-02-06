from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlmodel import Field


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None