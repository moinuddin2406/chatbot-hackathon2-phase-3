from typing import Dict, Any, Optional
from uuid import uuid4
import asyncio
import sys
import os

# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from sqlmodel import create_engine, Session
from models import Task

# Use the same database URL as the main app
# Import the main config using sys.path manipulation
import sys
import os
# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from config import settings  # Import from main app config
database_url = settings.DATABASE_URL

# Create a local engine instance to avoid circular imports
# For SQLite, we need to add check_same_thread=False for multiple thread access
if "sqlite" in database_url.lower():
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(database_url)


class MockMCPClient:
    def __init__(self):
        # Simulate a working client without requiring an external server
        # Use the main app's database engine instead of in-memory storage
        pass

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock implementation that simulates tool calls using the real database
        """
        # Simulate network delay
        await asyncio.sleep(0.1)

        if tool_name == "add_task":
            return await self.add_task(params.get("user_id"), params.get("title"), params.get("description"))
        elif tool_name == "list_tasks":
            return await self.list_tasks(params.get("user_id"), params.get("status"))
        elif tool_name == "complete_task":
            return await self.complete_task(params.get("user_id"), params.get("task_id"))
        elif tool_name == "update_task":
            return await self.update_task(
                params.get("user_id"),
                params.get("task_id"),
                title=params.get("title"),
                description=params.get("description"),
                completed=params.get("completed")
            )
        elif tool_name == "delete_task":
            return await self.delete_task(params.get("user_id"), params.get("task_id"))
        else:
            return {
                "success": False,
                "error": {"code": "UNKNOWN_TOOL", "message": f"Unknown tool: {tool_name}"}
            }

    # Specific tool methods for better organization
    async def add_task(self, user_id: str, title: str, description: Optional[str] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
        with Session(engine) as session:
            # Convert due_date string to datetime if provided
            from datetime import datetime
            due_date_obj = None
            if due_date:
                try:
                    due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    # If parsing fails, try other formats
                    try:
                        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
                    except ValueError:
                        # If all parsing fails, ignore the due date
                        due_date_obj = None
            
            task = Task(
                user_id=user_id,
                title=title,
                description=description or "",
                completed=False,
                due_date=due_date_obj
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            # Convert to dictionary format
            task_dict = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }

        return {
            "success": True,
            "data": task_dict
        }

    async def list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        with Session(engine) as session:
            query = session.query(Task).filter(Task.user_id == user_id)
            
            if status and status != "all":
                if status == "completed":
                    query = query.filter(Task.completed == True)
                elif status == "pending":
                    query = query.filter(Task.completed == False)
                    
            tasks = query.all()
            
            # Convert to dictionary format
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
                tasks_list.append(task_dict)

        return {
            "success": True,
            "data": tasks_list
        }

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.query(Task).filter(
                Task.id == task_id, 
                Task.user_id == user_id
            ).first()
            
            if task:
                task.completed = True
                session.add(task)
                session.commit()
                session.refresh(task)
                
                # Convert to dictionary format
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
                
                return {
                    "success": True,
                    "data": task_dict
                }
            else:
                return {
                    "success": False,
                    "error": {"code": "TASK_NOT_FOUND", "message": f"Task {task_id} not found for user {user_id}"}
                }

    async def update_task(self, user_id: str, task_id: str, **kwargs) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.query(Task).filter(
                Task.id == task_id, 
                Task.user_id == user_id
            ).first()
            
            if task:
                # Update task with provided data
                for key, value in kwargs.items():
                    if hasattr(task, key) and value is not None:
                        setattr(task, key, value)

                session.add(task)
                session.commit()
                session.refresh(task)
                
                # Convert to dictionary format
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
                
                return {
                    "success": True,
                    "data": task_dict
                }
            else:
                return {
                    "success": False,
                    "error": {"code": "TASK_NOT_FOUND", "message": f"Task {task_id} not found for user {user_id}"}
                }

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        with Session(engine) as session:
            task = session.query(Task).filter(
                Task.id == task_id, 
                Task.user_id == user_id
            ).first()
            
            if task:
                session.delete(task)
                session.commit()
                
                return {
                    "success": True,
                    "data": {"message": f"Task {task_id} deleted successfully"}
                }
            else:
                return {
                    "success": False,
                    "error": {"code": "TASK_NOT_FOUND", "message": f"Task {task_id} not found for user {user_id}"}
                }


# Global instance of the mock MCP client
mock_mcp_client = MockMCPClient()