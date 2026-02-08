from typing import Dict, Any, List
from ..models.chat_models import Message


def serialize_conversation_history(messages: List[Message]) -> List[Dict[str, Any]]:
    """
    Serialize conversation history for transmission or storage
    """
    serialized = []
    for message in messages:
        serialized.append({
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "tool_calls": message.tool_calls,
            "created_at": message.created_at.isoformat() if message.created_at else None
        })
    return serialized


def deserialize_conversation_history(serialized_messages: List[Dict[str, Any]]) -> List[Message]:
    """
    Deserialize conversation history from storage or transmission
    """
    # This function would typically recreate Message objects from the serialized data
    # For now, we'll return the list as-is since we're working with Pydantic models
    # that handle serialization/deserialization automatically
    return serialized_messages  # Placeholder implementation


def format_message_for_display(message: Message) -> Dict[str, Any]:
    """
    Format a message for display in the UI
    """
    return {
        "id": message.id,
        "sender": message.role,
        "content": message.content,
        "timestamp": message.created_at.isoformat() if message.created_at else None,
        "has_tool_calls": message.tool_calls is not None
    }


def get_last_n_messages(messages: List[Message], n: int) -> List[Message]:
    """
    Get the last N messages from a conversation
    """
    return messages[-n:] if len(messages) >= n else messages


def filter_messages_by_role(messages: List[Message], role: str) -> List[Message]:
    """
    Filter messages by role (user or assistant)
    """
    return [msg for msg in messages if msg.role == role]