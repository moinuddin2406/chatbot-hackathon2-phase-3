import html
import re
from typing import Union


def sanitize_input(input_text: Union[str, None]) -> Union[str, None]:
    """
    Sanitize user input to prevent injection attacks
    """
    if input_text is None:
        return None
        
    # Remove null bytes which could be dangerous
    sanitized = input_text.replace('\x00', '')
    
    # Escape HTML characters to prevent XSS
    sanitized = html.escape(sanitized)
    
    # Remove potentially dangerous patterns
    # This is a basic example - in a real implementation, you might want to use
    # a more comprehensive sanitization library like bleach
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized


def sanitize_conversation_id(conversation_id: str) -> str:
    """
    Sanitize conversation ID to ensure it's a valid UUID format
    """
    # Basic UUID validation (without importing uuid for efficiency)
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    if not uuid_pattern.match(conversation_id):
        raise ValueError("Invalid conversation ID format")
    return conversation_id


def sanitize_user_id(user_id: str) -> str:
    """
    Sanitize user ID to prevent injection attacks
    """
    # Basic validation - ensure user_id contains only alphanumeric characters and hyphens/underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        raise ValueError("Invalid user ID format")
    return user_id


def sanitize_task_title(title: str) -> str:
    """
    Sanitize task title
    """
    if len(title) > 255:
        raise ValueError("Task title exceeds maximum length of 255 characters")
    
    return sanitize_input(title) or ""


def sanitize_task_description(description: str) -> str:
    """
    Sanitize task description
    """
    if len(description) > 1000:
        raise ValueError("Task description exceeds maximum length of 1000 characters")
    
    return sanitize_input(description) or ""