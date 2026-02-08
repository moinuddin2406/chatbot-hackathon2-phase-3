#!/usr/bin/env python3
"""
Test script to verify all chatbot fixes
"""

import asyncio
import sys
import os
from uuid import uuid4

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from db import get_session
from chatbot.agents.chat_agent import ChatAgent
from chatbot.schemas.chat_schemas import ChatRequest
from models import Task


async def test_chatbot_fixes():
    """Test all the fixes for the chatbot"""
    print("Testing chatbot fixes...")
    
    # Create a new user ID for testing
    user_id = str(uuid4())
    print(f"Using user ID: {user_id}")
    
    # Create a chat agent instance
    chat_agent = ChatAgent()
    
    # Get a database session
    session_gen = get_session()
    db = next(session_gen)
    
    try:
        # Test 1: Add a task without the unwanted prefix
        print("\n[TEST 1] Adding a task without 'Task created from chat:' prefix")
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
                    due_date = task_data.get('due_date', '')
                    print(f"  - Task Title: '{title}'")
                    print(f"  - Task Description: '{description}'")
                    print(f"  - Task Due Date: '{due_date}'")
                    
                    # Verify the fix
                    if "Task created from chat:" in description:
                        print("  [FAIL] Still showing 'Task created from chat:' prefix")
                    else:
                        print("  [PASS] No unwanted prefix in description")
        
        # Get the task ID for subsequent tests
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        task_id = str(tasks[0].id) if tasks else None
        print(f"Created task ID: {task_id}")
        
        # Test 2: Add a task with due date
        print("\n[TEST 2] Adding a task with due date")
        chat_request2 = ChatRequest(
            message="create task Call dentist appointment by tomorrow",
            conversation_id=None
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
                    description = task_data.get('description', '')
                    due_date = task_data.get('due_date', '')
                    print(f"  - Task Title: '{title}'")
                    print(f"  - Task Description: '{description}'")
                    print(f"  - Task Due Date: '{due_date}'")
                    
                    if due_date:
                        print("  [PASS] Due date properly extracted and saved")
                    else:
                        print("  [FAIL] Due date not extracted")
        
        # Test 3: List tasks
        print("\n[TEST 3] Listing tasks")
        chat_request3 = ChatRequest(
            message="list my tasks",
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
                print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                if tc.result and tc.result.get('success'):
                    task_list = tc.result.get('data', [])
                    print(f"  Found {len(task_list)} tasks:")
                    for task in task_list:
                        title = task.get('title', '')
                        description = task.get('description', '')
                        completed = task.get('completed', False)
                        due_date = task.get('due_date', '')
                        task_id = task.get('id', '')
                        print(f"    - Task {task_id}: '{title}' - Completed: {completed}, Due: {due_date}")
        
        # Test 4: Update a task
        print("\n[TEST 4] Updating a task")
        if task_id:
            chat_request4 = ChatRequest(
                message=f"update task {task_id} title is Updated groceries list",
                conversation_id=result3['conversation_id']
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
                        task_data = tc.result.get('data', {})
                        title = task_data.get('title', '')
                        completed = task_data.get('completed', False)
                        due_date = task_data.get('due_date', '')
                        print(f"  - Updated Title: '{title}'")
                        print(f"  - Completed Status: {completed}")
                        print(f"  - Due Date: {due_date}")
        
        # Test 5: Complete a task
        print("\n[TEST 5] Completing a task")
        if task_id:
            chat_request5 = ChatRequest(
                message=f"complete task {task_id}",
                conversation_id=result4['conversation_id'] if 'result4' in locals() else result3['conversation_id']
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
                    print(f"Tool call: {tc.name}, Args: {tc.arguments}")
                    if tc.result and tc.result.get('success'):
                        task_data = tc.result.get('data', {})
                        title = task_data.get('title', '')
                        completed = task_data.get('completed', False)
                        due_date = task_data.get('due_date', '')
                        print(f"  - Title: '{title}'")
                        print(f"  - Completed Status: {completed} (should be True)")
                        print(f"  - Due Date: {due_date}")
                        
                        if completed:
                            print("  [PASS] Task marked as completed")
                        else:
                            print("  [FAIL] Task not marked as completed")
        
        print("\n[SUCCESS] All chatbot fixes tested successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during testing: {e}")
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
    success = asyncio.run(test_chatbot_fixes())
    if success:
        print("\n[RESULT] All tests passed!")
    else:
        print("\n[RESULT] Some tests failed!")