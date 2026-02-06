from typing import List, Optional
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_tasks_by_user_id(self, user_id: str) -> List[Task]:
        """Get all tasks for a specific user."""
        statement = select(Task).where(Task.user_id == user_id)
        results = self.session.exec(statement)
        return results.all()

    def get_task_by_id_and_user(self, task_id: int, user_id: str) -> Optional[Task]:
        """Get a specific task by ID for a specific user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.session.exec(statement)
        return result.first()

    def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create a new task."""
        task_data_dict = task_data.model_dump()
        task_data_dict['user_id'] = user_id
        task = Task(**task_data_dict)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update_task(self, task_id: int, user_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        task = self.get_task_by_id_and_user(task_id, user_id)
        if not task:
            return None

        # Update only the fields that are provided
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Manually update the updated_at field
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int, user_id: str) -> bool:
        """Delete a task."""
        task = self.get_task_by_id_and_user(task_id, user_id)
        if not task:
            return False
        
        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_completion(self, task_id: int, user_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self.get_task_by_id_and_user(task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed

        # Update the updated_at field
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task