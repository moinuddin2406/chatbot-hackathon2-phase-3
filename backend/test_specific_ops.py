#!/usr/bin/env python3
"""
Focused test to identify issues with update, edit, and complete operations
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_specific_operations():
    """Test specific operations that are reported as not working"""
    print("Testing specific operations that are not working...")
    
    mock_client = MockCohereClient()
    
    # Test cases for operations that should work but aren't
    test_cases = [
        # Update operations
        ("update task 123", "update_task"),
        ("update task 123 title is new title", "update_task"),
        ("edit task 456", "update_task"),
        ("edit task 456 description is new description", "update_task"),
        
        # Complete operations
        ("complete task 789", "complete_task"),
        ("finish task 789", "complete_task"),
        ("mark task 789 as done", "complete_task"),
        
        # Delete operations (should work)
        ("delete task 321", "delete_task"),
        ("remove task 321", "delete_task"),
        
        # Add operations (should work)
        ("add task Test title", "add_task"),
    ]
    
    print(f"Running {len(test_cases)} focused tests...\n")
    
    passed = 0
    failed = 0
    
    for i, (message, expected_tool) in enumerate(test_cases, 1):
        print(f"Test {i}: {message}")
        result = mock_client.chat_with_tools(message, [], [])
        
        if result['tool_calls']:
            actual_tool = result['tool_calls'][0]['name']
            if actual_tool == expected_tool:
                print(f"  SUCCESS: Correctly detected as {actual_tool}")
                print(f"  Parameters: {result['tool_calls'][0]['parameters']}")
                passed += 1
            else:
                print(f"  ERROR: Expected {expected_tool}, got {actual_tool}")
                failed += 1
        else:
            if expected_tool is None:
                print(f"  SUCCESS: Correctly detected as no tool needed")
                passed += 1
            else:
                print(f"  ERROR: Expected {expected_tool}, got no tool")
                failed += 1
        
        print()
    
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\nAll operations are working correctly!")
    else:
        print(f"\n{failed} operations need fixing.")


if __name__ == "__main__":
    test_specific_operations()