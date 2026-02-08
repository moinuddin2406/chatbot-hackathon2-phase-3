#!/usr/bin/env python3
"""
Test script to verify the authentication fix for the 403 error
"""

import sys
import os
from unittest.mock import Mock, patch
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from chatbot.routes.chat_routes import chat_endpoint
from chatbot.schemas.chat_schemas import ChatRequest
from sqlmodel import Session
from fastapi import HTTPException

async def test_authentication_validation():
    """Test that the authentication validation works correctly"""
    print("Testing authentication validation in chat endpoint...")
    
    # Create mock dependencies
    mock_db = Mock(spec=Session)
    mock_chat_request = ChatRequest(message="Test message")
    
    # Test 1: Valid case where current_user_id matches user_id
    print("\nTest 1: Valid case where authenticated user matches requested user")
    try:
        # This should work without raising an exception
        with patch('chatbot.middleware.auth.auth_middleware') as mock_auth:
            mock_auth.get_current_user = Mock(return_value="valid-user-id")
            
            # Mock the chat agent to avoid actual processing
            with patch('chatbot.agents.chat_agent.chat_agent') as mock_agent:
                mock_agent.process_message = Mock(return_value={
                    "conversation_id": str(uuid4()),
                    "response": "Test response",
                    "tool_calls": None
                })
                
                # Also mock the validation functions
                with patch('chatbot.utils.validation.validate_user_exists', return_value=True):
                    result = await chat_endpoint(
                        user_id="valid-user-id",
                        chat_request=mock_chat_request,
                        current_user_id="valid-user-id",
                        db=mock_db
                    )
                    print(f"SUCCESS: Valid case passed: {result}")
                    
    except Exception as e:
        print(f"ERROR: Valid case failed unexpectedly: {e}")
        return False

    # Test 2: Invalid case where current_user_id doesn't match user_id
    print("\nTest 2: Invalid case where authenticated user doesn't match requested user")
    try:
        with patch('chatbot.middleware.auth.auth_middleware') as mock_auth:
            mock_auth.get_current_user = Mock(return_value="different-user-id")
            
            # This should raise an HTTPException with 403 status
            try:
                result = await chat_endpoint(
                    user_id="target-user-id",
                    chat_request=mock_chat_request,
                    current_user_id="different-user-id",
                    db=mock_db
                )
                print("ERROR: Invalid case should have raised an exception but didn't")
                return False
            except HTTPException as e:
                if e.status_code == 403:
                    print(f"SUCCESS: Invalid case correctly raised 403: {e.detail if hasattr(e, 'detail') else str(e)}")
                else:
                    print(f"ERROR: Invalid case raised wrong status code {e.status_code}: {e}")
                    return False
            except Exception as e:
                print(f"ERROR: Invalid case raised unexpected exception: {e}")
                return False
                
    except Exception as e:
        print(f"ERROR: Error during invalid case test: {e}")
        return False

    print("\nSUCCESS: All authentication validation tests passed!")
    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_authentication_validation())
    if success:
        print("\nAuthentication fix verification: PASSED!")
    else:
        print("\nAuthentication fix verification: FAILED!")