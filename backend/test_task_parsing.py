#!/usr/bin/env python3
"""
Test script to verify the improved task parsing in the mock client
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '.')

from chatbot.clients.mock_client import MockCohereClient


def test_task_parsing():
    """Test the improved task parsing functionality"""
    print("Testing improved task parsing...")
    
    mock_client = MockCohereClient()
    
    # Test case 1: Original message
    message1 = "add a task description is exercise title is one two and due2/25/2026"
    print(f"\nTest 1 - Message: {message1}")
    
    result1 = mock_client.chat_with_tools(message1, [], [])
    print(f"Text response: {result1['text']}")
    print(f"Tool calls: {result1['tool_calls']}")
    
    if result1['tool_calls']:
        for call in result1['tool_calls']:
            if call['name'] == 'add_task':
                print(f"  - Title: {call['parameters']['title']}")
                print(f"  - Description: {call['parameters']['description']}")
    
    # Test case 2: Another variation
    message2 = "create a new task with title is workout and description is daily exercise routine"
    print(f"\nTest 2 - Message: {message2}")
    
    result2 = mock_client.chat_with_tools(message2, [], [])
    print(f"Text response: {result2['text']}")
    print(f"Tool calls: {result2['tool_calls']}")
    
    if result2['tool_calls']:
        for call in result2['tool_calls']:
            if call['name'] == 'add_task':
                print(f"  - Title: {call['parameters']['title']}")
                print(f"  - Description: {call['parameters']['description']}")
    
    # Test case 3: Simple add task
    message3 = "add task Buy groceries"
    print(f"\nTest 3 - Message: {message3}")
    
    result3 = mock_client.chat_with_tools(message3, [], [])
    print(f"Text response: {result3['text']}")
    print(f"Tool calls: {result3['tool_calls']}")
    
    if result3['tool_calls']:
        for call in result3['tool_calls']:
            if call['name'] == 'add_task':
                print(f"  - Title: {call['parameters']['title']}")
                print(f"  - Description: {call['parameters']['description']}")
    
    print("\nTest completed!")


if __name__ == "__main__":
    test_task_parsing()