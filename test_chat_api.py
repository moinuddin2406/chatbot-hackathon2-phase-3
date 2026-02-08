import requests
import json

# Test the chat endpoint
url = "http://localhost:8000/api/testuser/chat"
headers = {
    "Content-Type": "application/json"
}
data = {
    "message": "Add a task called 'Test task'"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", str(e))