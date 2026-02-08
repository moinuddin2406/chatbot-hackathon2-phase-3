#!/usr/bin/env python3
"""
Test script to verify the tool_calls column fix
"""

import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from db import get_session
from chatbot.services.conversation_service import create_conversation
from chatbot.models.chat_models import Message as MessageModel
from models import User
from sqlmodel import Session
import json


def test_message_creation_with_tool_calls():
    """Test creating messages with tool_calls field"""
    print("Testing message creation with tool_calls field...")
    
    # Get a database session
    session_gen = get_session()
    db = next(session_gen)
    
    try:
        # Create a new user ID
        new_user_id = str(uuid4())
        print(f"Using new user ID: {new_user_id}")
        
        # Create a conversation
        conversation = create_conversation(db, user_id=new_user_id)
        print(f"Created conversation: {conversation.id}")
        
        # Create a message with tool_calls (should now work without error)
        user_message = MessageModel(
            conversation_id=conversation.id,
            user_id=new_user_id,
            role="user",
            content="Test message with tool calls"
        )
        db.add(user_message)
        
        # Create an assistant message with tool_calls
        assistant_message = MessageModel(
            conversation_id=conversation.id,
            user_id=new_user_id,  # The assistant is acting on behalf of the user
            role="assistant",
            content="Test response",
            tool_calls=json.dumps([{"name": "test_tool", "arguments": {"param": "value"}}]) if True else None
        )
        db.add(assistant_message)
        
        # Commit the transaction (this would previously fail due to missing column)
        db.commit()
        print("Successfully saved messages with tool_calls to database!")
        
        # Verify the messages were saved
        from sqlalchemy import text
        result = db.execute(text("SELECT * FROM messages WHERE conversation_id = :conv_id ORDER BY created_at ASC"), 
                           {"conv_id": conversation.id})
        messages = result.fetchall()
        print(f"Retrieved {len(messages)} messages from database")
        
        for msg in messages:
            print(f"  - Message ID: {msg[0]}, Role: {msg[3]}, Content: {msg[4][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"Error creating messages: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Close the session
        try:
            next(session_gen)
        except StopIteration:
            pass  # Generator exhausted, which is expected


if __name__ == "__main__":
    success = test_message_creation_with_tool_calls()
    if success:
        print("\nTest PASSED: The tool_calls column fix is working correctly!")
    else:
        print("\nTest FAILED: The tool_calls column fix is not working!")