from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Cohere API Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")  # Default to empty string

    # Database Configuration - Use the same as main app
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Secret Key for JWT tokens
    secret_key: str = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-here-make-it-long-and-random")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MCP Server Configuration
    mcp_server_url: str = "http://localhost:8001"

    # Logging Configuration
    log_level: str = "INFO"

    # Add the fields that are causing the validation error
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")
    
    # Add common environment variables that might be set
    next_public_api_base_url: str = os.getenv("NEXT_PUBLIC_API_BASE_URL", "")
    
    class Config:
        # Allow extra fields to prevent validation errors
        extra = "allow"


settings = Settings()