import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from backend.chatbot.models.chat_models import Task, Conversation, Message
from backend.chatbot.services.message_service import create_message, get_messages_for_conversation
from backend.chatbot.schemas.chat_schemas import MessageCreate


@pytest.fixture
def mock_db():
    """Mock database session for testing"""
    db = MagicMock(spec=Session)
    return db


def test_task_creation():
    """Test creating a new task"""
    task = Task(
        user_id="user123",
        title="Test Task",
        description="Test Description",
        completed=False
    )
    
    assert task.user_id == "user123"
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.id is not None  # UUID should be generated


def test_conversation_creation():
    """Test creating a new conversation"""
    conversation = Conversation(
        user_id="user123"
    )
    
    assert conversation.user_id == "user123"
    assert conversation.id is not None  # UUID should be generated
    assert conversation.messages == []  # Relationship should be empty initially


def test_message_creation():
    """Test creating a new message"""
    message = Message(
        conversation_id="conv123",
        user_id="user123",
        role="user",
        content="Test message"
    )
    
    assert message.conversation_id == "conv123"
    assert message.user_id == "user123"
    assert message.role == "user"
    assert message.content == "Test message"
    assert message.id is not None  # UUID should be generated


def test_message_service_create_message(mock_db):
    """Test creating a message using the message service"""
    message_data = MessageCreate(
        conversation_id="conv123",
        user_id="user123",
        role="user",
        content="Test message"
    )
    
    # Mock the database operations
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    created_message = create_message(mock_db, message_data)
    
    # Verify the message was added to the database
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    
    # Verify the returned message has the correct data
    assert created_message.conversation_id == "conv123"
    assert created_message.user_id == "user123"
    assert created_message.role == "user"
    assert created_message.content == "Test message"


def test_message_service_get_messages_for_conversation(mock_db):
    """Test retrieving messages for a conversation"""
    # Mock the query result
    mock_message = Message(
        id="msg123",
        conversation_id="conv123",
        user_id="user123",
        role="user",
        content="Test message"
    )
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [mock_message]
    mock_db.query.return_value = mock_query
    
    messages = get_messages_for_conversation(mock_db, "conv123")
    
    # Verify the query was called correctly
    mock_db.query.assert_called_once_with(Message)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once()
    
    # Verify the returned message
    assert len(messages) == 1
    assert messages[0].id == "msg123"
    assert messages[0].content == "Test message"