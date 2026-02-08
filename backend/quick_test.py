import sys
sys.path.insert(0, '.')
from chatbot.clients.mock_client import MockCohereClient

mock_client = MockCohereClient()

# Test cases for better title/description extraction
test_cases = [
    ('add task Buy groceries from the market', 'add_task'),
    ('create task Schedule doctor appointment', 'add_task'),
    ('new task Call mom tonight', 'add_task'),
    ('add a task Walk the dog in the morning', 'add_task'),
    ('update task 123 title is Updated groceries list', 'update_task'),
    ('update task 456 title is New title and description is New description', 'update_task'),
    ('edit task 789 title is Edited task', 'update_task'),
]

print(f'Running {len(test_cases)} tests...\n')

for i, (message, expected_tool) in enumerate(test_cases, 1):
    print(f'Test {i}: {message}')
    result = mock_client.chat_with_tools(message, [], [])

    if result['tool_calls']:
        actual_tool = result['tool_calls'][0]['name']
        params = result['tool_calls'][0]['parameters']

        print(f'  Detected: {actual_tool}')
        print(f'  Parameters: {params}')

        # Check if the expected tool was detected
        if actual_tool == expected_tool:
            print(f'  SUCCESS: Correct tool detected')

            # Check title/description extraction
            if actual_tool == 'add_task':
                title = params.get('title', '')
                description = params.get('description', '')

                if title and title != 'New Task':
                    print(f'  SUCCESS: Title properly extracted: "{title}"')
                else:
                    print(f'  FAIL: Title not properly extracted: "{title}"')

            elif actual_tool == 'update_task':
                title = params.get('title', '')
                description = params.get('description', '')
                task_id = params.get('task_id', '')

                print(f'  Task ID: {task_id}')
                if title:
                    print(f'  SUCCESS: Title for update: "{title}"')
                else:
                    print(f'  WARNING: No title provided for update')
        else:
            print(f'  FAIL: Expected {expected_tool}, got {actual_tool}')
    else:
        print(f'  FAIL: No tool detected')

    print()

print('UI display fix test completed!')