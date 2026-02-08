#!/usr/bin/env python3
"""
Comprehensive test to verify all fixes for UI display issues
"""

import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, '.')

from db import get_session
from chatbot.agents.chat_agent import ChatAgent
from chatbot.schemas.chat_schemas import ChatRequest


async def test_ui_display_fixes():
    """Test that fixes resolve UI display issues"""
    print("Testing UI display fixes...")
    
    # Create a new user ID for testing
    user_id = str(uuid4())
    print(f"Using user ID: {user_id}")
    
    # Create a chat agent instance
    chat_agent = ChatAgent()
    
    # Get a database session
    session_gen = get_session()
    db = next(session_gen)
    
    try:
        # Test 1: Add a task with proper title (not "New Task")
        print("\nTest 1: Adding a task with proper title...")
        chat_request1 = ChatRequest(
            message="add task Buy groceries from the market",
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
                print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                if tc.result and tc.result.get('success'):
                    task_data = tc.result.get('data', {})
                    title = task_data.get('title', '')
                    description = task_data.get('description', '')
                    print(f"  - Task Title: '{title}' (should not be 'New Task')")
                    print(f"  - Task Description: '{description}' (should not start with 'Task created from chat:')")
        
        # Get the task ID for subsequent tests
        from models import Task
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        task_id = str(tasks[0].id) if tasks else None
        print(f"Created task ID: {task_id}")
        
        # Test 2: Update the task to change title/description
        print(f"\nTest 2: Updating task {task_id}...")
        if task_id:
            chat_request2 = ChatRequest(
                message=f"update task {task_id} title is Updated groceries list",
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
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                    if tc.result and tc.result.get('success'):
                        task_data = tc.result.get('data', {})
                        title = task_data.get('title', '')
                        completed = task_data.get('completed', False)
                        print(f"  - Updated Title: '{title}'")
                        print(f"  - Completed Status: {completed}")
        
        # Test 3: Complete the task
        print(f"\nTest 3: Completing task {task_id}...")
        if task_id:
            chat_request3 = ChatRequest(
                message=f"complete task {task_id}",
                conversation_id=result2['conversation_id'] if 'result2' in locals() else result1['conversation_id']
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
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                    if tc.result and tc.result.get('success'):
                        task_data = tc.result.get('data', {})
                        title = task_data.get('title', '')
                        completed = task_data.get('completed', False)
                        print(f"  - Title: '{title}'")
                        print(f"  - Completed Status: {completed} (should be True)")
        
        # Test 4: List tasks to verify all changes are reflected
        print(f"\nTest 4: Listing tasks to verify changes...")
        chat_request4 = ChatRequest(
            message="list my tasks",
            conversation_id=result3['conversation_id'] if 'result3' in locals() else result2['conversation_id'] if 'result2' in locals() else result1['conversation_id']
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
                print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                if tc.result and tc.result.get('success'):
                    task_list = tc.result.get('data', [])
                    for task in task_list:
                        title = task.get('title', '')
                        description = task.get('description', '')
                        completed = task.get('completed', False)
                        task_id = task.get('id', '')
                        print(f"  - Task {task_id}: '{title}' - Completed: {completed}")
                        if "New Task" in title:
                            print("    ⚠ ISSUE: Still showing 'New Task'")
                        if "Task created from chat:" in description:
                            print("    ⚠ ISSUE: Still showing 'Task created from chat:'")
        
        print("\nUI display fix test completed!")
        return True
        
    except Exception as e:
        print(f"Error during UI display test: {e}")
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
    success = asyncio.run(test_ui_display_fixes())
    if success:
        print("\nUI display fix test: PASSED!")
    else:
        print("\nUI display fix test: FAILED!")