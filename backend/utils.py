import logging
from fastapi import HTTPException, status
from typing import Any, Dict


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_error(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    """Generic error handler"""
    logger.error(detail)
    raise HTTPException(status_code=status_code, detail=detail)


def log_api_call(endpoint: str, user_id: str, action: str):
    """Log API calls for monitoring and debugging"""
    logger.info(f"API Call: {endpoint} | User: {user_id} | Action: {action}")


class APIError(Exception):
    """Custom API error class"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)