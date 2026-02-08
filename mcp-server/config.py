from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./mcp_server.db"
    
    # Secret Key for validation
    secret_key: str = "your-secret-key-here-make-it-long-and-random"
    algorithm: str = "HS256"
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings()