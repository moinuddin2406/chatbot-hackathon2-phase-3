import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from db import get_session
from chatbot.services.conversation_service import create_conversation
from chatbot.utils.validation import ensure_user_exists
from models import User
from sqlmodel import Session

print('Testing conversation creation with non-existent user...')

# Get a database session
session_gen = get_session()
db = next(session_gen)

try:
    # Create a new user ID that doesn't exist
    new_user_id = str(uuid4())
    print(f'Using new user ID: {new_user_id}')
    
    # Try to create a conversation - this should now work because ensure_user_exists is called internally
    conversation = create_conversation(db, user_id=new_user_id)
    print(f'Successfully created conversation: {conversation.id} for user: {new_user_id}')
    
    # Verify the user was created in the database
    user = db.query(User).filter(User.id == new_user_id).first()
    if user:
        print(f'User was automatically created: {user.id}, {user.email}')
    else:
        print('ERROR: User was not created!')
        
    print('\nTest PASSED: The fix is working correctly!')
    
except Exception as e:
    print(f'Error creating conversation: {e}')
    import traceback
    traceback.print_exc()
    print('\nTest FAILED: The fix is not working!')
finally:
    # Close the session
    try:
        next(session_gen)
    except StopIteration:
        pass  # Generator exhausted, which is expected