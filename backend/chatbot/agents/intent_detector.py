from typing import Dict, Any, Optional
import re


class IntentDetector:
    """
    Detects user intent from natural language input
    """
    
    def __init__(self):
        # Define patterns for different intents
        self.patterns = {
            "add_task": [
                r"add.*task.*",
                r"create.*task.*",
                r"new.*task.*",
                r"make.*task.*",
                r"remind.*me.*to.*",
                r"need.*to.*",
                r"have.*to.*",
                r"should.*",
                r"must.*"
            ],
            "list_tasks": [
                r"show.*task.*",
                r"list.*task.*",
                r"what.*task.*",
                r"my.*task.*",
                r"pending.*task.*",
                r"incomplete.*task.*",
                r"active.*task.*",
                r"current.*task.*"
            ],
            "complete_task": [
                r"complete.*task.*",
                r"finish.*task.*",
                r"done.*with.*task.*",
                r"mark.*task.*done",
                r"check.*off.*task.*",
                r"accomplish.*task.*"
            ],
            "update_task": [
                r"change.*task.*",
                r"modify.*task.*",
                r"update.*task.*",
                r"edit.*task.*",
                r"rename.*task.*"
            ],
            "delete_task": [
                r"delete.*task.*",
                r"remove.*task.*",
                r"cancel.*task.*",
                r"get rid of.*task.*",
                r"eliminate.*task.*"
            ]
        }
    
    def detect_intent(self, message: str) -> Optional[str]:
        """
        Detect the intent from the user message
        """
        message_lower = message.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        # If no specific intent is detected, return a general intent
        return "general_query"
    
    def extract_task_details(self, message: str) -> Dict[str, Any]:
        """
        Extract task details from a message (title, description, etc.)
        """
        # This is a simplified extraction - in a real implementation,
        # you'd use more sophisticated NLP techniques
        message_lower = message.lower()
        
        # Remove common phrases that indicate task creation
        cleaned_message = message
        for phrase in ["add a task to", "create a task to", "new task:", "i need to", "i have to", "remind me to"]:
            if phrase in message_lower:
                cleaned_message = message[len(phrase):].strip()
                break
        
        # Extract title and description
        title = cleaned_message.split(".")[0].strip() if cleaned_message else message
        description = ""  # In a real implementation, you'd extract more details
        
        return {
            "title": title,
            "description": description
        }
    
    def extract_task_id(self, message: str) -> Optional[str]:
        """
        Extract task ID from a message if present
        """
        # Look for patterns like "task 1", "task #1", "#1", etc.
        patterns = [
            r"task\s+#?(\d+)",
            r"#(\d+)",
            r"task\s+(\d+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None


# Global instance of the intent detector
intent_detector = IntentDetector()