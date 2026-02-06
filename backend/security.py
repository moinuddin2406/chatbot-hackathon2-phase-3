import hashlib
from fastapi import HTTPException, status
from typing import Dict, Any
from models import Task
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    Uses SHA-256 pre-hashing to handle passwords longer than 72 bytes.
    """
    # Pre-hash the plain password with SHA-256 to handle long passwords
    password_digest = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(password_digest, hashed_password)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.
    Uses SHA-256 pre-hashing to handle passwords longer than 72 bytes.
    """
    # Pre-hash the password with SHA-256 to handle long passwords
    password_digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(password_digest)


def verify_user_owns_resource(user_id: str, resource: Any) -> bool:
    """
    Verify that the authenticated user owns the resource they're trying to access.
    For tasks, this checks if the user_id matches the task's user_id.
    """
    if hasattr(resource, 'user_id'):
        return resource.user_id == user_id
    return False


def check_user_id_match(token_user_id: str, url_user_id: str) -> bool:
    """
    Check if the user ID in the JWT token matches the user ID in the URL.
    Returns True if they match, raises an exception if they don't.
    """
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in URL"
        )
    return True