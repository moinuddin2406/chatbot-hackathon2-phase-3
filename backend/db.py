from sqlmodel import create_engine, Session, SQLModel
from config import settings
from models import User, Task  # Import all models to register them with SQLModel
from chatbot.models.chat_models import Conversation, Message  # Import chatbot models too
import os

# Create the database engine
# Use settings.DATABASE_URL which gets the value from environment variables
# Only add SQLite-specific connect_args if using SQLite
if "sqlite" in settings.DATABASE_URL.lower():
    engine = create_engine(
        settings.DATABASE_URL, 
        echo=True,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # For PostgreSQL and other databases, don't include SQLite-specific args
    engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session