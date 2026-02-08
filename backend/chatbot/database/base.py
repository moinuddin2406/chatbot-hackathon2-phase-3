import sys
import os
from sqlmodel import create_engine, Session

# Add the backend directory to the Python path to allow absolute imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from config import settings  # Import from main app config


# Create the database engine - use main app's database URL
# Only add SQLite-specific connect_args if using SQLite
if "sqlite" in settings.DATABASE_URL.lower():
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # For PostgreSQL and other databases, don't include SQLite-specific args
    engine = create_engine(settings.DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session