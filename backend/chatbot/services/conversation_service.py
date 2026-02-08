from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from ..models.chat_models import Conversation, Message
from ..schemas.chat_schemas import Message as MessageSchema


def generate_conversation_id() -> str:
    """Generate a unique conversation ID"""
    return str(uuid4())


def create_conversation(db: Session, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
    """Create a new conversation for a user"""
    from ..utils.validation import ensure_user_exists
    
    try:
        # Ensure the user exists before creating the conversation
        if not ensure_user_exists(user_id, db):
            raise ValueError(f"Could not ensure user with id {user_id} exists in the database")
        
        if conversation_id is None:
            conversation_id = generate_conversation_id()

        conversation = Conversation(
            id=conversation_id,
            user_id=user_id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    except Exception as e:
        # Rollback the transaction on error
        db.rollback()
        raise e


def get_conversation(db: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
    """Get a specific conversation for a user"""
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()


def get_conversations_for_user(db: Session, user_id: str) -> List[Conversation]:
    """Get all conversations for a specific user"""
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()


def get_conversation_history(db: Session, conversation_id: str, limit: int = 50, offset: int = 0) -> List[MessageSchema]:
    """Get the conversation history for a specific conversation with pagination"""
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).offset(offset).limit(limit).all()
    
    # Convert to schema format
    history = []
    for msg in messages:
        history.append(MessageSchema(
            id=msg.id,
            conversation_id=msg.conversation_id,
            user_id=msg.user_id,
            role=msg.role,
            content=msg.content,
            tool_calls=msg.tool_calls,
            created_at=msg.created_at
        ))
    
    return history


def get_conversation_history_count(db: Session, conversation_id: str) -> int:
    """Get the count of messages in a conversation"""
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).count()


def update_conversation_timestamp(db: Session, conversation_id: str):
    """Update the updated_at timestamp for a conversation"""
    from sqlalchemy.sql import func
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.updated_at = func.now()
        db.commit()


def delete_conversation(db: Session, conversation_id: str, user_id: str) -> bool:
    """Delete a conversation for a user"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False