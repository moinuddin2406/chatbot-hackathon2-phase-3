#!/usr/bin/env python3
"""
Test script to verify that all task functionalities work correctly after the fixes
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_all_task_functions():
    """Test all task functions to ensure they work correctly after the fixes"""
    print("Testing all task functions after fixes...")
    
    mock_client = MockCohereClient()
    
    # Test cases for each function
    test_cases = [
        # Add task cases
        ("add a task description is exercise routine title is morning workout and due 2/25/2026", "add_task"),
        ("create a new task with title is grocery shopping and description is buy milk and bread", "add_task"),
        ("add task Buy groceries", "add_task"),
        
        # Update task cases
        ("update task 123 with title is updated workout and description is updated exercise routine", "update_task"),
        ("edit task 456 title is evening workout", "update_task"),
        ("change task 789 and description is new description", "update_task"),
        
        # List task cases
        ("list my tasks", "list_tasks"),
        ("show my tasks", "list_tasks"),
        
        # Complete task cases
        ("complete task 999", "complete_task"),
        ("finish task 888", "complete_task"),
        
        # Delete task cases
        ("delete task 555", "delete_task"),
        ("remove task 444", "delete_task"),
    ]
    
    for i, (message, expected_tool) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {message}")
        result = mock_client.chat_with_tools(message, [], [])
        
        if result['tool_calls']:
            actual_tool = result['tool_calls'][0]['name']
            if actual_tool == expected_tool:
                print(f"  SUCCESS: Correctly detected as {actual_tool}")
                print(f"  Parameters: {result['tool_calls'][0]['parameters']}")
            else:
                print(f"  ERROR: Expected {expected_tool}, got {actual_tool}")
        else:
            if expected_tool is None:
                print(f"  SUCCESS: Correctly detected as no tool needed")
            else:
                print(f"  ERROR: Expected {expected_tool}, got no tool")
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    test_all_task_functions()