#!/usr/bin/env python3
"""
Test common problematic patterns that users might try
"""

import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from db import get_session
from chatbot.agents.chat_agent import ChatAgent
from chatbot.schemas.chat_schemas import ChatRequest


async def test_common_patterns():
    """Test common patterns that might not work as expected"""
    print("Testing common problematic patterns...")
    
    # Create a new user ID for testing
    user_id = str(uuid4())
    print(f"Using user ID: {user_id}")
    
    # Create a chat agent instance
    chat_agent = ChatAgent()
    
    # Get a database session
    session_gen = get_session()
    db = next(session_gen)
    
    try:
        # Test 1: Add a task
        print("\nTest 1: Adding a task...")
        chat_request1 = ChatRequest(
            message="add task My test task",
            conversation_id=None
        )
        
        result1 = await chat_agent.process_message(
            user_id=user_id,
            message=chat_request1.message,
            conversation_id=chat_request1.conversation_id,
            db=db
        )
        
        print(f"Added task response: {result1['response']}")
        if result1['tool_calls']:
            for tc in result1['tool_calls']:
                print(f"Tool call: {tc.name}, Args: {tc.arguments}")
        
        # Get the task ID for subsequent tests
        from models import Task
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        task_id = str(tasks[0].id) if tasks else None
        print(f"Created task ID: {task_id}")
        
        # Test various update patterns
        update_patterns = [
            f"update task {task_id}",
            f"update task {task_id} with new title",
            f"edit task {task_id}",
            f"edit task {task_id} title is edited title",
            f"change task {task_id} description is changed description"
        ]
        
        current_conversation_id = result1['conversation_id']
        
        for i, pattern in enumerate(update_patterns, 2):
            print(f"\nTest {i}: Trying pattern - {pattern}")
            chat_request = ChatRequest(
                message=pattern,
                conversation_id=current_conversation_id
            )
            
            try:
                result = await chat_agent.process_message(
                    user_id=user_id,
                    message=chat_request.message,
                    conversation_id=chat_request.conversation_id,
                    db=db
                )
                
                print(f"  Response: {result['response']}")
                if result['tool_calls']:
                    for tc in result['tool_calls']:
                        print(f"  Tool call: {tc.name}, Args: {tc.arguments}")
                        if tc.result and tc.result.get('success'):
                            print(f"  ✓ Operation successful")
                        else:
                            print(f"  ⚠ Operation may have failed")
                
                current_conversation_id = result['conversation_id']
            except Exception as e:
                print(f"  ✗ Error with pattern '{pattern}': {e}")
        
        # Test various complete patterns
        complete_patterns = [
            f"complete task {task_id}",
            f"finish task {task_id}",
            f"mark task {task_id} as done",
            f"complete task {task_id} now"
        ]
        
        for i, pattern in enumerate([idx for idx in range(len(update_patterns)+2, len(update_patterns)+2+len(complete_patterns))], len(update_patterns)+2):
            pattern_idx = i - (len(update_patterns)+2)
            pattern = complete_patterns[pattern_idx]
            print(f"\nTest {i}: Trying complete pattern - {pattern}")
            chat_request = ChatRequest(
                message=pattern,
                conversation_id=current_conversation_id
            )
            
            try:
                result = await chat_agent.process_message(
                    user_id=user_id,
                    message=chat_request.message,
                    conversation_id=chat_request.conversation_id,
                    db=db
                )
                
                print(f"  Response: {result['response']}")
                if result['tool_calls']:
                    for tc in result['tool_calls']:
                        print(f"  Tool call: {tc.name}, Args: {tc.arguments}")
                        if tc.result and tc.result.get('success'):
                            print(f"  ✓ Operation successful")
                        else:
                            print(f"  ⚠ Operation may have failed")
                
                current_conversation_id = result['conversation_id']
            except Exception as e:
                print(f"  ✗ Error with pattern '{pattern}': {e}")
        
        print("\n✓ All common pattern tests completed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during common pattern test: {e}")
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
    import asyncio
    success = asyncio.run(test_common_patterns())
    if success:
        print("\nCommon pattern test: PASSED!")
    else:
        print("\nCommon pattern test: FAILED!")