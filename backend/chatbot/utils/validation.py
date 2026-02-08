from typing import Optional
from fastapi import HTTPException, status
from ..config import settings


def validate_user_access(user_id: str, requested_user_id: str) -> bool:
    """
    Validates that the user has access to resources belonging to requested_user_id.
    In a real implementation, this would check permissions, roles, etc.
    For now, we assume the user_id from the token matches the requested_user_id.
    """
    # In a real implementation, this would validate the user's token
    # and check if they have access to the requested resource
    return user_id == requested_user_id


def validate_user_exists(user_id: str, db=None) -> bool:
    """
    Validates that the user exists in the system.
    If db is provided, queries the user database to check if the user exists.
    Otherwise, performs basic validation (non-empty string).
    """
    if db is None:
        # For backward compatibility, if no db is provided, do basic validation
        return user_id is not None and len(user_id.strip()) > 0
    else:
        # Query the database to check if the user exists
        from models import User  # Import here to avoid circular imports
        
        user = db.query(User).filter(User.id == user_id).first()
        return user is not None


def ensure_user_exists(user_id: str, db) -> bool:
    """
    Ensures that the user exists in the database.
    If the user doesn't exist, creates a new user record.
    Returns True if user exists (either already existed or was created).
    """
    from models import User  # Import here to avoid circular imports
    
    # Import the password hashing function from main backend using sys.path manipulation
    import sys
    import os
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    from security import hash_password

    # Check if user already exists
    existing_user = db.query(User).filter(User.id == user_id).first()

    if existing_user:
        return True

    # User doesn't exist, create a new user
    try:
        # Create a new user with the given ID
        # Use a default/placeholder password that gets hashed
        default_password = "default_password_for_placeholder_user"
        hashed_default_password = hash_password(default_password)
        
        new_user = User(
            id=user_id,
            email=f"{user_id}@example.com",  # Placeholder email
            name=f"User {user_id[:8]}",      # Use part of the ID as name
            hashed_password=hashed_default_password  # Required field
        )

        db.add(new_user)
        # Flush the session to make the user available for foreign key constraints
        # but don't commit yet - let the calling function handle the full transaction
        db.flush()

        return True
    except Exception as e:
        print(f"Error creating user {user_id}: {e}")
        return False


def sanitize_input(input_text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    if input_text is None:
        return None
        
    # Remove null bytes which could be dangerous
    sanitized = input_text.replace('\x00', '')
    
    # In a real implementation, you might want to use a library like bleach
    # for more comprehensive sanitization depending on your use case
    
    return sanitized