#!/usr/bin/env python3
"""
Test script to verify the enhanced multilingual chatbot functionality
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_multilingual_chatbot():
    """Test the enhanced multilingual chatbot functionality"""
    print("Testing enhanced multilingual chatbot functionality...")
    
    mock_client = MockCohereClient()
    
    # Test cases for each function in both English and Urdu
    test_cases = [
        # English Add task cases
        ("add a task description is exercise routine title is morning workout and due 2/25/2026", "add_task"),
        ("create a new task with title is grocery shopping and description is buy milk and bread", "add_task"),
        
        # Urdu Add task cases
        ("task add karo title is morning exercise aur description is daily routine", "add_task"),
        
        # English Update task cases
        ("update task 123 with title is updated workout and description is updated exercise routine", "update_task"),
        ("edit task 456 title is evening workout", "update_task"),
        
        # Urdu Update task cases
        ("task 789 ko update karo title is updated routine aur description is new description", "update_task"),
        
        # English List task cases
        ("list my tasks", "list_tasks"),
        ("show my tasks", "list_tasks"),
        
        # Urdu List task cases
        ("mera tasks dekho", "list_tasks"),
        
        # English Complete task cases
        ("complete task 999", "complete_task"),
        ("finish task 888", "complete_task"),
        ("mark task 777 as done", "complete_task"),
        
        # Urdu Complete task cases
        ("task 555 ko complete karo", "complete_task"),
        ("task 444 ho gaya", "complete_task"),
        
        # English Delete task cases
        ("delete task 333", "delete_task"),
        ("remove task 222", "delete_task"),
        
        # Urdu Delete task cases
        ("yeh task 111 delete kar do", "delete_task"),
        ("task 666 nikal do", "delete_task"),
    ]
    
    print(f"Running {len(test_cases)} test cases...\n")
    
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
        print("\n🎉 All tests passed! The chatbot correctly handles multilingual commands.")
    else:
        print(f"\n⚠️  {failed} tests failed. Some functionality needs attention.")


if __name__ == "__main__":
    test_multilingual_chatbot()