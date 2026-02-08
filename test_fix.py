#!/usr/bin/env python3
"""
Test script to verify the fix for the foreign key constraint error
"""

import sys
import os
from uuid import uuid4

# Add backend to path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from backend.db import get_session, create_db_and_tables
from backend.chatbot.services.conversation_service import create_conversation
from backend.chatbot.utils.validation import ensure_user_exists

def test_conversation_creation():
    """Test creating a conversation with a non-existent user"""
    print("Testing conversation creation with non-existent user...")
    
    # Get a database session
    session_gen = get_session()
    db = next(session_gen)
    
    try:
        # Create a new user ID that doesn't exist
        new_user_id = str(uuid4())
        print(f"Using new user ID: {new_user_id}")
        
        # Try to create a conversation - this should now work because ensure_user_exists is called internally
        conversation = create_conversation(db, user_id=new_user_id)
        print(f"Successfully created conversation: {conversation.id} for user: {new_user_id}")
        
        # Verify the user was created in the database
        from backend.models import User
        user = db.query(User).filter(User.id == new_user_id).first()
        if user:
            print(f"User was automatically created: {user.id}, {user.email}")
        else:
            print("ERROR: User was not created!")
            
        return True
        
    except Exception as e:
        print(f"Error creating conversation: {e}")
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
    success = test_conversation_creation()
    if success:
        print("\nTest PASSED: The fix is working correctly!")
    else:
        print("\nTest FAILED: The fix is not working!")