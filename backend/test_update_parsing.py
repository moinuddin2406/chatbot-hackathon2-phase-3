#!/usr/bin/env python3
"""
Test script to verify the improved update task functionality
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_update_task_parsing():
    """Test the improved update task parsing functionality"""
    print("Testing improved update task parsing...")
    
    mock_client = MockCohereClient()
    
    # Test case 1: Update task with title and description
    message1 = "update task 123 with title is updated workout and description is updated exercise routine"
    print(f"\nTest 1 - Message: {message1}")
    
    result1 = mock_client.chat_with_tools(message1, [], [])
    print(f"Tool calls: {result1['tool_calls']}")
    
    if result1['tool_calls']:
        for call in result1['tool_calls']:
            print(f"  - Name: {call['name']}")
            print(f"  - Parameters: {call['parameters']}")
    
    # Test case 2: Edit task
    message2 = "edit task 456 title is evening workout"
    print(f"\nTest 2 - Message: {message2}")
    
    result2 = mock_client.chat_with_tools(message2, [], [])
    print(f"Tool calls: {result2['tool_calls']}")
    
    if result2['tool_calls']:
        for call in result2['tool_calls']:
            print(f"  - Name: {call['name']}")
            print(f"  - Parameters: {call['parameters']}")
    
    # Test case 3: Change task
    message3 = "change task 789 and description is new description"
    print(f"\nTest 3 - Message: {message3}")
    
    result3 = mock_client.chat_with_tools(message3, [], [])
    print(f"Tool calls: {result3['tool_calls']}")
    
    if result3['tool_calls']:
        for call in result3['tool_calls']:
            print(f"  - Name: {call['name']}")
            print(f"  - Parameters: {call['parameters']}")
    
    # Test case 4: Complete task
    message4 = "complete task 999"
    print(f"\nTest 4 - Message: {message4}")
    
    result4 = mock_client.chat_with_tools(message4, [], [])
    print(f"Tool calls: {result4['tool_calls']}")
    
    if result4['tool_calls']:
        for call in result4['tool_calls']:
            print(f"  - Name: {call['name']}")
            print(f"  - Parameters: {call['parameters']}")
    
    # Test case 5: Delete task
    message5 = "delete task 555"
    print(f"\nTest 5 - Message: {message5}")
    
    result5 = mock_client.chat_with_tools(message5, [], [])
    print(f"Tool calls: {result5['tool_calls']}")
    
    if result5['tool_calls']:
        for call in result5['tool_calls']:
            print(f"  - Name: {call['name']}")
            print(f"  - Parameters: {call['parameters']}")
    
    print("\nTest completed!")


if __name__ == "__main__":
    test_update_task_parsing()