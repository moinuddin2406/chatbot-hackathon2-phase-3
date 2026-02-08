from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from ..models.task import Task
from ..schemas.task_schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task in the database"""
    db_task = Task(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a specific user"""
    return db.query(Task).filter(and_(Task.id == task_id, Task.user_id == user_id)).first()


def get_tasks(db: Session, user_id: str, status: str = "all") -> List[Task]:
    """Get all tasks for a specific user with optional status filter"""
    query = db.query(Task).filter(Task.user_id == user_id)
    
    if status == "pending":
        query = query.filter(Task.completed == False)
    elif status == "completed":
        query = query.filter(Task.completed == True)
    
    return query.all()


def update_task(db: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a specific task for a specific user"""
    db_task = db.query(Task).filter(and_(Task.id == task_id, Task.user_id == user_id)).first()
    
    if db_task:
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed
            
        db.commit()
        db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: str, user_id: str) -> bool:
    """Delete a specific task for a specific user"""
    db_task = db.query(Task).filter(and_(Task.id == task_id, Task.user_id == user_id)).first()
    
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    
    return False