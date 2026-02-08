from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from uuid import uuid4
from datetime import datetime
from ..database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }