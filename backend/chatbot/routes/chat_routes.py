import sys
import os
# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from ..schemas.chat_schemas import ChatRequest, ChatResponse
from ..database.base import get_db, engine  # Use the same engine as defined in base
from ..middleware.auth import auth_middleware
from ..agents.chat_agent import chat_agent
from ..models.chat_models import Conversation, Message
from ..utils.validation import validate_user_access, validate_user_exists
from ..errors.exceptions import unauthorized_access, validation_error
from models import Task, TaskCreate, TaskUpdate  # Import from main models using absolute import


router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user_id: str = Depends(auth_middleware.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        # Validate that the authenticated user has access to the requested user_id
        if current_user_id != user_id:
            raise unauthorized_access("user", user_id)
        
        # Validate that the user exists in the database
        if not validate_user_exists(user_id, db):
            raise unauthorized_access("user", user_id)

        # Validate the request
        if not chat_request.message or len(chat_request.message.strip()) == 0:
            raise validation_error("message", "Message cannot be empty")

        # Process the message using the chat agent
        result = await chat_agent.process_message(
            user_id=user_id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id,
            db=db
        )

        # Format the response
        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result.get("tool_calls")
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like authentication errors) so FastAPI handles them properly
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error in chat_endpoint: {e}")
        import traceback
        traceback.print_exc()

        # Return a response that includes the error for debugging
        return ChatResponse(
            conversation_id=chat_request.conversation_id or "unknown",
            response=f"Debug: Error occurred - {str(e)}",
            tool_calls=None
        )


# Task management endpoints that the chatbot can use
@router.get("/{user_id}/tasks", response_model=list)
async def get_tasks(
    user_id: str,
    current_user_id: str = Depends(auth_middleware.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for a specific user"""
    # Validate that the authenticated user has access to the requested user_id
    if current_user_id != user_id:
        raise unauthorized_access("user", user_id)
    
    # Use the same database session as the rest of the request
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=Task)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(auth_middleware.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for a specific user"""
    # Validate that the authenticated user has access to the requested user_id
    if current_user_id != user_id:
        raise unauthorized_access("user", user_id)
    
    # Use the same database session as the rest of the request
    task = Task(user_id=user_id, **task_data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=Task)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user_id: str = Depends(auth_middleware.get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific task for a user"""
    # Validate that the authenticated user has access to the requested user_id
    if current_user_id != user_id:
        raise unauthorized_access("user", user_id)
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task with provided data
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(auth_middleware.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific task for a user"""
    # Validate that the authenticated user has access to the requested user_id
    if current_user_id != user_id:
        raise unauthorized_access("user", user_id)
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}