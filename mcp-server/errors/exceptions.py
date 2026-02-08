from fastapi import HTTPException, status
from typing import Optional


class MCPTaskServerError(Exception):
    """Base exception class for MCP task server errors"""
    def __init__(self, error_code: str, message: str, details: Optional[dict] = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


def create_http_exception(
    status_code: int,
    error_code: str,
    message: str,
    details: Optional[dict] = None
) -> HTTPException:
    """Helper function to create standardized HTTP exceptions"""
    return HTTPException(
        status_code=status_code,
        detail={
            "error_code": error_code,
            "message": message,
            "details": details or {}
        }
    )


# Specific error helpers
def user_not_found(user_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="USER_NOT_FOUND",
        message=f"User with id {user_id} not found",
        details={"user_id": user_id}
    )


def task_not_found(task_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="TASK_NOT_FOUND",
        message=f"Task with id {task_id} not found",
        details={"task_id": task_id}
    )


def unauthorized_access(resource_type: str, resource_id: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_403_FORBIDDEN,
        error_code="USER_ACCESS_DENIED",
        message=f"Access denied to {resource_type} with id {resource_id}",
        details={"resource_type": resource_type, "resource_id": resource_id}
    )


def validation_error(field: str, message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        message=f"Validation error in field '{field}': {message}",
        details={"field": field, "error": message}
    )


def internal_error(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_ERROR",
        message=message,
        details={}
    )