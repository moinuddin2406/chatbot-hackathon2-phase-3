from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings


# Create the database engine
# Only add SQLite-specific connect_args if using SQLite
if "sqlite" in settings.database_url.lower():
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # For PostgreSQL and other databases, don't include SQLite-specific args
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()