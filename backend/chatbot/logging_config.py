import logging
from .config import settings


def setup_logging():
    """Configure logging based on settings"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)


def log_audit_event(event_type: str, user_id: str, details: dict = None):
    """
    Log an audit event for sensitive operations
    """
    logger = get_logger("audit")
    event_details = {
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "details": details or {}
    }
    logger.info(f"AUDIT_EVENT: {event_details}")


def log_sensitive_operation(operation: str, user_id: str, resource: str, resource_id: str = None):
    """
    Log sensitive operations for audit purposes
    """
    log_audit_event(
        event_type="SENSITIVE_OPERATION",
        user_id=user_id,
        details={
            "operation": operation,
            "resource": resource,
            "resource_id": resource_id
        }
    )