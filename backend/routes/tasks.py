from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
from db import get_session
from models import Task, TaskCreate, TaskUpdate
from auth import get_current_user
from security import check_user_id_match
from utils import log_api_call
from services.task_service import TaskService


# Create the router for task-related endpoints
router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Log the API call
    log_api_call("/tasks", user_id, "get_tasks")

    # Get tasks for the user
    task_service = TaskService(session)
    tasks = task_service.get_tasks_by_user_id(user_id)

    return tasks


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Ensure the task is created for the correct user
    # Log the API call
    log_api_call("/tasks", user_id, "create_task")

    # Create the task
    task_service = TaskService(session)
    task = task_service.create_task(task_data, user_id)

    return task


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Log the API call
    log_api_call(f"/tasks/{task_id}", user_id, "get_task")

    # Get the task
    task_service = TaskService(session)
    task = task_service.get_task_by_id_and_user(task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Log the API call
    log_api_call(f"/tasks/{task_id}", user_id, "update_task")

    # Update the task
    task_service = TaskService(session)
    task = task_service.update_task(task_id, user_id, task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Log the API call
    log_api_call(f"/tasks/{task_id}", user_id, "delete_task")

    # Delete the task
    task_service = TaskService(session)
    success = task_service.delete_task(task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify that the user ID in the token matches the user ID in the URL
    check_user_id_match(current_user.get("sub"), user_id)

    # Log the API call
    log_api_call(f"/tasks/{task_id}/complete", user_id, "toggle_completion")

    # Toggle task completion
    task_service = TaskService(session)
    task = task_service.toggle_completion(task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task