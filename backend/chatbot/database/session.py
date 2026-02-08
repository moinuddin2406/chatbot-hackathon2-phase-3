from .base import SessionLocal, get_db
from ..config import settings


def get_session():
    """
    Get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables
    """
    from .base import engine, Base
    Base.metadata.create_all(bind=engine)