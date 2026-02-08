from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from ..config import settings


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()
        
    async def get_current_user(self, request: Request):
        """
        Extract and validate the user from the authorization header
        """
        credentials: HTTPAuthorizationCredentials = await self.security.__call__(request)
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        token = credentials.credentials
        try:
            # Decode the JWT token to get user info
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            return user_id
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Create a global instance of the middleware
auth_middleware = AuthMiddleware()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt