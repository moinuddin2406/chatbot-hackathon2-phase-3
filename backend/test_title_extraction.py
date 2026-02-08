#!/usr/bin/env python3
"""
Test to verify the fixes for task title/description extraction
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_title_extraction():
    """Test the improved title/description extraction"""
    print("Testing improved title/description extraction...")
    
    mock_client = MockCohereClient()
    
    # Test cases for add task with better title/description extraction
    test_cases = [
        # Add task cases
        ("add task Buy groceries", "add_task"),
        ("add task Schedule meeting with John", "add_task"),
        ("create task Call dentist appointment", "add_task"),
        ("add a task Walk the dog", "add_task"),
        
        # Update task cases
        ("update task 123 title is updated title", "update_task"),
        ("edit task 456 description is updated description", "update_task"),
        ("change task 789 title is new title and description is new description", "update_task"),
    ]
    
    print(f"Running {len(test_cases)} tests...\n")
    
    for i, (message, expected_tool) in enumerate(test_cases, 1):
        print(f"Test {i}: {message}")
        result = mock_client.chat_with_tools(message, [], [])
        
        if result['tool_calls']:
            actual_tool = result['tool_calls'][0]['name']
            params = result['tool_calls'][0]['parameters']
            
            print(f"  Detected: {actual_tool}")
            print(f"  Parameters: {params}")
            
            # Check if title/description are properly extracted
            if actual_tool == "add_task":
                title = params.get('title', '')
                description = params.get('description', '')
                if title and "New Task" not in title:
                    print(f"  ✓ Title properly extracted: '{title}'")
                else:
                    print(f"  ⚠ Title not properly extracted: '{title}'")
                    
                if description and "Task created from chat:" not in description:
                    print(f"  ✓ Description properly extracted: '{description}'")
                else:
                    print(f"  ⚠ Description not properly extracted: '{description}'")
            
            elif actual_tool == "update_task":
                title = params.get('title', '')
                description = params.get('description', '')
                task_id = params.get('task_id', '')
                
                print(f"  Task ID: {task_id}")
                if title:
                    print(f"  ✓ Title for update: '{title}'")
                if description:
                    print(f"  ✓ Description for update: '{description}'")
        
        print()
    
    print("Title/description extraction test completed!")


if __name__ == "__main__":
    test_title_extraction()