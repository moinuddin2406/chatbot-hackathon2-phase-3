from sqlmodel import create_engine, Session, SQLModel
from config import settings
from models import User, Task  # Import all models to register them with SQLModel
import os

# Create the database engine
# Use settings.DATABASE_URL which gets the value from environment variables
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session