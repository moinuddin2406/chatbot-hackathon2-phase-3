import sys
import os
# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from typing import Dict, Any, List, Optional
from ..clients.cohere_client import cohere_client
from ..clients.mcp_client import mcp_client
from ..schemas.chat_schemas import ToolCall, ToolCallResult, Message
from ..models.chat_models import Conversation, Message as MessageModel
from models import Task  # Import Task from main models using absolute import
from sqlalchemy.orm import Session
import json


class ChatAgent:
    def __init__(self):
        self.cohere_client = cohere_client
        self.mcp_client = mcp_client

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str],
        db: Session
    ) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response
        """
        # Get conversation history if conversation_id is provided
        conversation_history = []
        if conversation_id:
            # Fetch conversation messages from database
            messages = db.query(MessageModel).filter(
                MessageModel.conversation_id == conversation_id
            ).order_by(MessageModel.created_at.asc()).all()

            # Convert to format expected by Cohere
            for msg in messages:
                conversation_history.append({
                    "role": msg.role,
                    "message": msg.content
                })
        else:
            # Ensure that the user exists in the database before creating a new conversation
            from ..utils.validation import ensure_user_exists
            if not ensure_user_exists(user_id, db):
                raise ValueError(f"Could not ensure user with id {user_id} exists in the database")
            
            # Create a new conversation
            from uuid import uuid4
            conversation_id = str(uuid4())
            new_conversation = Conversation(
                id=conversation_id,
                user_id=user_id
            )
            try:
                db.add(new_conversation)
                db.commit()
                db.refresh(new_conversation)  # Refresh to ensure the object is properly persisted
            except Exception as e:
                db.rollback()  # Rollback the transaction on error
                print(f"Error creating conversation: {e}")
                raise ValueError(f"Failed to create conversation for user {user_id}: {str(e)}")

        # Define tools that the AI can use
        tools = [
            {
                "name": "add_task",
                "description": "Add a new task for the user",
                "parameter_definitions": {
                    "user_id": {"type": "str", "required": True},
                    "title": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False}
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks for the user",
                "parameter_definitions": {
                    "user_id": {"type": "str", "required": True},
                    "status": {"type": "str", "required": False, "default": "all"}
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "user_id": {"type": "str", "required": True},
                    "task_id": {"type": "str", "required": True}
                }
            },
            {
                "name": "update_task",
                "description": "Update a task for the user",
                "parameter_definitions": {
                    "user_id": {"type": "str", "required": True},
                    "task_id": {"type": "str", "required": True},
                    "title": {"type": "str", "required": False},
                    "description": {"type": "str", "required": False},
                    "completed": {"type": "bool", "required": False}
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task for the user",
                "parameter_definitions": {
                    "user_id": {"type": "str", "required": True},
                    "task_id": {"type": "str", "required": True}
                }
            }
        ]

        # Call Cohere to process the message and determine if tools are needed
        try:
            cohere_response = self.cohere_client.chat_with_tools(
                message=message,
                conversation_history=conversation_history,
                tools=tools
            )
        except Exception as e:
            # If there's an error with the Cohere client, return a simple response
            print(f"Error with Cohere client: {e}")
            cohere_response = {
                "text": "Hi there! I'm your task assistant. How can I help you today?",
                "tool_calls": []
            }

        response_text = cohere_response["text"]
        tool_calls = cohere_response["tool_calls"]

        # Execute any required tool calls
        tool_results = []
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                parameters = tool_call["parameters"]

                # Ensure user_id is included in parameters
                parameters["user_id"] = user_id

                try:
                    # Execute the appropriate tool
                    if tool_name == "add_task":
                        result = await self.mcp_client.add_task(
                            user_id=parameters["user_id"],
                            title=parameters["title"],
                            description=parameters.get("description", "")
                        )
                    elif tool_name == "list_tasks":
                        result = await self.mcp_client.list_tasks(
                            user_id=parameters["user_id"],
                            status=parameters.get("status", "all")
                        )
                    elif tool_name == "complete_task":
                        result = await self.mcp_client.complete_task(
                            user_id=parameters["user_id"],
                            task_id=parameters["task_id"]
                        )
                    elif tool_name == "update_task":
                        result = await self.mcp_client.update_task(
                            user_id=parameters["user_id"],
                            task_id=parameters["task_id"],
                            title=parameters.get("title"),
                            description=parameters.get("description"),
                            completed=parameters.get("completed")
                        )
                    elif tool_name == "delete_task":
                        result = await self.mcp_client.delete_task(
                            user_id=parameters["user_id"],
                            task_id=parameters["task_id"]
                        )
                    else:
                        result = {
                            "success": False,
                            "error": {"code": "UNKNOWN_TOOL", "message": f"Unknown tool: {tool_name}"}
                        }
                except Exception as e:
                    print(f"Error executing tool {tool_name}: {e}")
                    result = {
                        "success": False,
                        "error": {"code": "EXECUTION_ERROR", "message": str(e)}
                    }

                tool_results.append({
                    "name": tool_name,
                    "arguments": parameters,
                    "result": result
                })

        # If there were tool calls, get the final response from Cohere
        if tool_results:
            try:
                response_text = self.cohere_client.process_tool_results(
                    original_message=message,
                    conversation_history=conversation_history,
                    tool_results=tool_results
                )
            except Exception as e:
                print(f"Error processing tool results: {e}")
                response_text = "I've processed your request. How else can I assist you?"

        # Ensure that the user exists in the database before saving messages
        from ..utils.validation import ensure_user_exists
        if not ensure_user_exists(user_id, db):
            raise ValueError(f"Could not ensure user with id {user_id} exists in the database")

        # Save the user message to the database
        user_message = MessageModel(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=message
        )
        db.add(user_message)

        # Save the assistant response to the database
        assistant_message = MessageModel(
            conversation_id=conversation_id,
            user_id=user_id,  # The assistant is acting on behalf of the user
            role="assistant",
            content=response_text,
            tool_calls=json.dumps(tool_results) if tool_results else None
        )
        db.add(assistant_message)

        # Update the conversation's updated_at timestamp
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            from sqlalchemy.sql import func
            conversation.updated_at = func.now()

        try:
            db.commit()
        except Exception as e:
            db.rollback()  # Rollback the transaction on error
            print(f"Error committing transaction: {e}")
            raise ValueError(f"Failed to save messages to database: {str(e)}")

        # Format the response
        formatted_tool_calls = [
            ToolCallResult(
                name=tool_result["name"],
                arguments=tool_result["arguments"],
                result=tool_result["result"]
            )
            for tool_result in tool_results
        ] if tool_results else None

        return {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": formatted_tool_calls
        }


# Global instance of the chat agent
chat_agent = ChatAgent()