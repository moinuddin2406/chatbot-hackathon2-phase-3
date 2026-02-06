import requests
import json

# Test the API endpoint directly
url = "http://127.0.0.1:8000/auth/register"

# Test with a password that is 73 characters long (should trigger validation)
payload = {
    "name": "Test User",
    "email": "test_validation_api@example.com",
    "password": "a" * 73  # 73 characters, should trigger validation error
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 422:  # Validation error status code
        print("Validation worked correctly!")
    else:
        print("Validation may not have worked as expected.")
        
except Exception as e:
    print(f"Error: {e}")