from typing import Dict, Any, Optional
from ..clients.mcp_client import mcp_client
from .intent_detector import intent_detector


class ToolRouter:
    """
    Routes intents to appropriate MCP tools
    """
    
    def __init__(self):
        self.mcp_client = mcp_client
        self.intent_detector = intent_detector
    
    async def route_intent(
        self,
        user_id: str,
        message: str,
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route the detected intent to the appropriate tool
        """
        # Detect the intent from the message
        intent = self.intent_detector.detect_intent(message)
        
        # Extract any relevant details
        task_details = self.intent_detector.extract_task_details(message)
        task_id = self.intent_detector.extract_task_id(message)
        
        # Route to the appropriate tool based on intent
        if intent == "add_task":
            return await self._handle_add_task(user_id, task_details)
        elif intent == "list_tasks":
            status = self._extract_status_from_message(message)
            return await self._handle_list_tasks(user_id, status)
        elif intent == "complete_task":
            return await self._handle_complete_task(user_id, task_id)
        elif intent == "update_task":
            return await self._handle_update_task(user_id, task_id, task_details)
        elif intent == "delete_task":
            return await self._handle_delete_task(user_id, task_id)
        else:
            # For general queries, return a response indicating the intent wasn't understood
            return {
                "success": False,
                "error": {"code": "UNKNOWN_INTENT", "message": f"Could not understand intent: {intent}"},
                "data": None
            }
    
    async def _handle_add_task(self, user_id: str, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the add_task intent
        """
        result = await self.mcp_client.add_task(
            user_id=user_id,
            title=task_details["title"],
            description=task_details["description"]
        )
        return result
    
    async def _handle_list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle the list_tasks intent
        """
        result = await self.mcp_client.list_tasks(
            user_id=user_id,
            status=status
        )
        return result
    
    async def _handle_complete_task(self, user_id: str, task_id: Optional[str]) -> Dict[str, Any]:
        """
        Handle the complete_task intent
        """
        if not task_id:
            return {
                "success": False,
                "error": {"code": "MISSING_TASK_ID", "message": "Task ID is required to complete a task"},
                "data": None
            }
        
        result = await self.mcp_client.complete_task(
            user_id=user_id,
            task_id=task_id
        )
        return result
    
    async def _handle_update_task(
        self,
        user_id: str,
        task_id: Optional[str],
        task_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle the update_task intent
        """
        if not task_id:
            return {
                "success": False,
                "error": {"code": "MISSING_TASK_ID", "message": "Task ID is required to update a task"},
                "data": None
            }
        
        # Prepare update parameters
        update_params = {}
        if task_details.get("title"):
            update_params["title"] = task_details["title"]
        if task_details.get("description"):
            update_params["description"] = task_details["description"]
        
        result = await self.mcp_client.update_task(
            user_id=user_id,
            task_id=task_id,
            **update_params
        )
        return result
    
    async def _handle_delete_task(self, user_id: str, task_id: Optional[str]) -> Dict[str, Any]:
        """
        Handle the delete_task intent
        """
        if not task_id:
            return {
                "success": False,
                "error": {"code": "MISSING_TASK_ID", "message": "Task ID is required to delete a task"},
                "data": None
            }
        
        result = await self.mcp_client.delete_task(
            user_id=user_id,
            task_id=task_id
        )
        return result
    
    def _extract_status_from_message(self, message: str) -> Optional[str]:
        """
        Extract status filter from message (pending, completed, all)
        """
        message_lower = message.lower()
        
        if "pending" in message_lower or "incomplete" in message_lower or "active" in message_lower:
            return "pending"
        elif "completed" in message_lower or "done" in message_lower or "finished" in message_lower:
            return "completed"
        else:
            return "all"


# Global instance of the tool router
tool_router = ToolRouter()