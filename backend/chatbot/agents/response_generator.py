from typing import Dict, Any, List, Optional
from ..schemas.chat_schemas import ToolCallResult


class ResponseGenerator:
    """
    Generates user-friendly responses based on tool results
    """
    
    def __init__(self):
        pass
    
    def generate_response(self, intent: str, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate a user-friendly response based on the tool result
        """
        if not tool_result.get("success", False):
            return self._generate_error_response(tool_result, original_message)
        
        # Generate response based on intent and result
        if intent == "add_task":
            return self._generate_add_task_response(tool_result, original_message)
        elif intent == "list_tasks":
            return self._generate_list_tasks_response(tool_result, original_message)
        elif intent == "complete_task":
            return self._generate_complete_task_response(tool_result, original_message)
        elif intent == "update_task":
            return self._generate_update_task_response(tool_result, original_message)
        elif intent == "delete_task":
            return self._generate_delete_task_response(tool_result, original_message)
        else:
            return f"I processed your request: {original_message}. Let me know if you need anything else!"
    
    def _generate_error_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate a response for when a tool call fails
        """
        error_info = tool_result.get("error", {})
        error_code = error_info.get("code", "UNKNOWN_ERROR")
        error_message = error_info.get("message", "An unknown error occurred")
        
        # Provide user-friendly error messages based on error code
        if error_code == "TASK_NOT_FOUND":
            return "I couldn't find that task. Could you check the task ID or provide more details?"
        elif error_code == "USER_ACCESS_DENIED":
            return "I'm sorry, but you don't have permission to access that task."
        elif error_code == "VALIDATION_ERROR":
            return f"I couldn't process your request: {error_message}. Could you rephrase that?"
        else:
            return f"I'm sorry, but I encountered an issue processing your request: {error_message}. Could you try again?"
    
    def _generate_add_task_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate response for adding a task
        """
        task_data = tool_result.get("data", {})
        task_title = task_data.get("title", "the task")
        
        return f"I've added the task '{task_title}' to your list. Is there anything else you'd like to do?"
    
    def _generate_list_tasks_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate response for listing tasks
        """
        task_data = tool_result.get("data", {})
        tasks = task_data.get("tasks", [])
        
        if not tasks:
            return "You don't have any tasks on your list right now."
        
        # Count pending vs completed tasks
        pending_count = sum(1 for task in tasks if not task.get("completed", False))
        completed_count = len(tasks) - pending_count
        
        if "pending" in original_message.lower() or "incomplete" in original_message.lower():
            if pending_count == 0:
                return "You don't have any pending tasks right now."
            else:
                return f"You have {pending_count} pending task{'s' if pending_count != 1 else ''}."
        elif "completed" in original_message.lower() or "done" in original_message.lower():
            if completed_count == 0:
                return "You haven't completed any tasks yet."
            else:
                return f"You have completed {completed_count} task{'s' if completed_count != 1 else ''}."
        else:
            return f"You have {len(tasks)} task{'s' if len(tasks) != 1 else ''} in total. {pending_count} are pending and {completed_count} are completed."
    
    def _generate_complete_task_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate response for completing a task
        """
        task_data = tool_result.get("data", {})
        task_id = task_data.get("task_id", "the task")
        
        return f"I've marked task {task_id} as completed. Great job!"
    
    def _generate_update_task_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate response for updating a task
        """
        task_data = tool_result.get("data", {})
        task_id = task_data.get("task_id", "the task")
        
        return f"I've updated task {task_id} for you. Is there anything else you'd like to change?"
    
    def _generate_delete_task_response(self, tool_result: Dict[str, Any], original_message: str) -> str:
        """
        Generate response for deleting a task
        """
        task_data = tool_result.get("data", {})
        task_id = task_data.get("task_id", "the task")
        
        return f"I've deleted task {task_id} from your list."
    
    def generate_general_response(self, original_message: str) -> str:
        """
        Generate a general response when no specific intent is detected
        """
        return f"I received your message: '{original_message}'. How can I assist you with your tasks today?"


# Global instance of the response generator
response_generator = ResponseGenerator()