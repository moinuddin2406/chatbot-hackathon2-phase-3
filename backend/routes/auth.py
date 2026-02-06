from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from db import get_session
from models import User, UserCreate, UserPublic
from auth import create_access_token
from security import verify_password, hash_password
from datetime import timedelta
import logging
import uuid

# Set up logging
logger = logging.getLogger(__name__)

# Create the router for authentication-related endpoints
router = APIRouter()

@router.post("/register", response_model=UserPublic)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Create new user
    user = User(
        id=user_id,
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"New user registered: {user.email}")

    return user


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Find user by email
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes expiration
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name},
        expires_delta=access_token_expires
    )

    logger.info(f"User logged in: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }