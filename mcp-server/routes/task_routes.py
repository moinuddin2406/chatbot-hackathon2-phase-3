from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database.base import get_db
from ..schemas.task_schemas import TaskCreate, TaskUpdate, Task
from ..database.task_operations.task_crud import (
    create_task as crud_create_task,
    get_task as crud_get_task,
    get_tasks as crud_get_tasks,
    update_task as crud_update_task,
    delete_task as crud_delete_task
)
from ..utils.validation import validate_user_access


router = APIRouter()


@router.post("/add_task")
def add_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task for a user"""
    try:
        # Validate user access
        if not validate_user_access(task_data.user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Create the task
        db_task = crud_create_task(db, task_data)
        
        return {
            "success": True,
            "data": {
                "task_id": db_task.id,
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "created_at": db_task.created_at.isoformat() if db_task.created_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "CREATE_TASK_ERROR", "message": str(e)}
        }


@router.post("/list_tasks")
def list_tasks(user_id: str, status: str = "all", db: Session = Depends(get_db)):
    """List tasks for a user with optional status filter"""
    try:
        # Validate user access
        if not validate_user_access(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get tasks
        tasks = crud_get_tasks(db, user_id, status)
        
        # Format the tasks for response
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })
        
        return {
            "success": True,
            "data": {
                "tasks": formatted_tasks
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "LIST_TASKS_ERROR", "message": str(e)}
        }


@router.post("/complete_task")
def complete_task(user_id: str, task_id: str, db: Session = Depends(get_db)):
    """Mark a task as completed"""
    try:
        # Validate user access
        if not validate_user_access(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get the current task to update
        current_task = crud_get_task(db, task_id, user_id)
        if not current_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update the task to mark as completed
        task_update = TaskUpdate(completed=True)
        updated_task = crud_update_task(db, task_id, user_id, task_update)
        
        return {
            "success": True,
            "data": {
                "task_id": updated_task.id,
                "completed": updated_task.completed,
                "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "COMPLETE_TASK_ERROR", "message": str(e)}
        }


@router.post("/update_task")
def update_task(user_id: str, task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task for a user"""
    try:
        # Validate user access
        if not validate_user_access(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Update the task
        updated_task = crud_update_task(db, task_id, user_id, task_update)
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "success": True,
            "data": {
                "task_id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description,
                "completed": updated_task.completed,
                "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "UPDATE_TASK_ERROR", "message": str(e)}
        }


@router.post("/delete_task")
def delete_task(user_id: str, task_id: str, db: Session = Depends(get_db)):
    """Delete a task for a user"""
    try:
        # Validate user access
        if not validate_user_access(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Delete the task
        success = crud_delete_task(db, task_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "deleted": True
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": {"code": "DELETE_TASK_ERROR", "message": str(e)}
        }