from sqlalchemy.orm import Session
from typing import List
from ..models.chat_models import Message, Conversation
from ..schemas.chat_schemas import MessageCreate


def create_message(db: Session, message: MessageCreate) -> Message:
    """Create a new message in the database"""
    db_message = Message(
        conversation_id=message.conversation_id,
        user_id=message.user_id,
        role=message.role,
        content=message.content,
        tool_calls=message.tool_calls
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_for_conversation(db: Session, conversation_id: str) -> List[Message]:
    """Get all messages for a specific conversation"""
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()


def get_recent_messages(db: Session, conversation_id: str, limit: int = 10) -> List[Message]:
    """Get the most recent messages for a conversation (for context)"""
    return db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()


def delete_message(db: Session, message_id: str) -> bool:
    """Delete a specific message"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False