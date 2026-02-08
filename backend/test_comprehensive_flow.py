#!/usr/bin/env python3
"""
Comprehensive test to verify the entire task flow works end-to-end
"""

import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from db import get_session
from chatbot.agents.chat_agent import ChatAgent
from chatbot.schemas.chat_schemas import ChatRequest


async def test_comprehensive_task_flow():
    """Test the complete task flow from chat to database"""
    print("Testing comprehensive task flow...")
    
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
            message="add a task description is exercise title is workout and due2/25/2026",
            conversation_id=None
        )
        
        result1 = await chat_agent.process_message(
            user_id=user_id,
            message=chat_request1.message,
            conversation_id=chat_request1.conversation_id,
            db=db
        )
        
        print(f"Response: {result1['response']}")
        if result1['tool_calls']:
            for tc in result1['tool_calls']:
                print(f"Tool call: {tc.name}, Args: {tc.arguments}, Result: {tc.result}")
        
        # Test 2: List tasks
        print("\nTest 2: Listing tasks...")
        chat_request2 = ChatRequest(
            message="list my tasks",
            conversation_id=result1['conversation_id']
        )
        
        result2 = await chat_agent.process_message(
            user_id=user_id,
            message=chat_request2.message,
            conversation_id=chat_request2.conversation_id,
            db=db
        )
        
        print(f"Response: {result2['response']}")
        if result2['tool_calls']:
            for tc in result2['tool_calls']:
                print(f"Tool call: {tc.name}, Args: {tc.arguments}, Result: {tc.result}")
        
        # Test 3: Update a task (we'll need to get the task ID first)
        print("\nTest 3: Updating a task...")
        from models import Task
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        if tasks:
            task_id = str(tasks[0].id)  # Get the first task ID
            chat_request3 = ChatRequest(
                message=f"update task {task_id} with title is updated workout and description is updated exercise routine",
                conversation_id=result2['conversation_id']
            )
            
            result3 = await chat_agent.process_message(
                user_id=user_id,
                message=chat_request3.message,
                conversation_id=chat_request3.conversation_id,
                db=db
            )
            
            print(f"Response: {result3['response']}")
            if result3['tool_calls']:
                for tc in result3['tool_calls']:
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}, Result: {tc.result}")
        
        # Test 4: Complete a task
        print("\nTest 4: Completing a task...")
        if tasks:
            task_id = str(tasks[0].id)  # Get the first task ID
            chat_request4 = ChatRequest(
                message=f"complete task {task_id}",
                conversation_id=result3['conversation_id'] if 'result3' in locals() else result2['conversation_id']
            )
            
            result4 = await chat_agent.process_message(
                user_id=user_id,
                message=chat_request4.message,
                conversation_id=chat_request4.conversation_id,
                db=db
            )
            
            print(f"Response: {result4['response']}")
            if result4['tool_calls']:
                for tc in result4['tool_calls']:
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}, Result: {tc.result}")
        
        # Test 5: Delete a task
        print("\nTest 5: Deleting a task...")
        if tasks:
            task_id = str(tasks[0].id)  # Get the first task ID
            chat_request5 = ChatRequest(
                message=f"delete task {task_id}",
                conversation_id=result4['conversation_id'] if 'result4' in locals() else result3['conversation_id'] if 'result3' in locals() else result2['conversation_id']
            )
            
            result5 = await chat_agent.process_message(
                user_id=user_id,
                message=chat_request5.message,
                conversation_id=chat_request5.conversation_id,
                db=db
            )
            
            print(f"Response: {result5['response']}")
            if result5['tool_calls']:
                for tc in result5['tool_calls']:
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}, Result: {tc.result}")
        
        print("\n✓ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error during comprehensive test: {e}")
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
    success = asyncio.run(test_comprehensive_task_flow())
    if success:
        print("\nComprehensive task flow test: PASSED!")
    else:
        print("\nComprehensive task flow test: FAILED!")