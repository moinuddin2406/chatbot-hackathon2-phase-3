from fastapi import HTTPException, status
from typing import Optional
from enum import Enum


class ErrorCode(str, Enum):
    # User-related errors
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ACCESS_DENIED = "USER_ACCESS_DENIED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    
    # Task-related errors
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    TASK_INVALID_DATA = "TASK_INVALID_DATA"
    
    # Conversation-related errors
    CONVERSATION_NOT_FOUND = "CONVERSATION_NOT_FOUND"
    CONVERSATION_INVALID_DATA = "CONVERSATION_INVALID_DATA"
    
    # Message-related errors
    MESSAGE_NOT_FOUND = "MESSAGE_NOT_FOUND"
    MESSAGE_INVALID_DATA = "MESSAGE_INVALID_DATA"
    
    # AI/Tool-related errors
    AI_SERVICE_ERROR = "AI_SERVICE_ERROR"
    TOOL_EXECUTION_ERROR = "TOOL_EXECUTION_ERROR"
    
    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"


class ChatbotError(Exception):
    """Base exception class for chatbot-related errors"""
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[dict] = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


def create_http_exception(
    status_code: int,
    error_code: ErrorCode,
    message: str,
    details: Optional[dict] = None
) -> HTTPException:
    """Helper function to create standardized HTTP exceptions"""
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code.value,
            "message": message,
            "details": details or {}
        }
    )


# Specific error helpers
def user_not_found(user_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code=ErrorCode.USER_NOT_FOUND,
        message=f"User with id {user_id} not found",
        details={"user_id": user_id}
    )


def task_not_found(task_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code=ErrorCode.TASK_NOT_FOUND,
        message=f"Task with id {task_id} not found",
        details={"task_id": task_id}
    )


def conversation_not_found(conversation_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code=ErrorCode.CONVERSATION_NOT_FOUND,
        message=f"Conversation with id {conversation_id} not found",
        details={"conversation_id": conversation_id}
    )


def unauthorized_access(resource_type: str, resource_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_403_FORBIDDEN,
        error_code=ErrorCode.USER_ACCESS_DENIED,
        message=f"Access denied to {resource_type} with id {resource_id}",
        details={"resource_type": resource_type, "resource_id": resource_id}
    )


def validation_error(field: str, message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code=ErrorCode.VALIDATION_ERROR,
        message=f"Validation error in field '{field}': {message}",
        details={"field": field, "error": message}
    )


def internal_error(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code=ErrorCode.INTERNAL_ERROR,
        message=message,
        details={}
    )