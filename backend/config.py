from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Environment variables
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")  # Using SQLite for local testing
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Add the fields that are causing the validation error
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    NEXT_PUBLIC_API_BASE_URL: str = os.getenv("NEXT_PUBLIC_API_BASE_URL", "")

    class Config:
        env_file = ".env"
        # Allow extra fields to prevent validation errors
        extra = "allow"


# Create a single instance of settings
settings = Settings()