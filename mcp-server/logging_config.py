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