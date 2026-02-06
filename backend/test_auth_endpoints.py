import requests

# Test the auth endpoints directly
base_url = "http://127.0.0.1:8000"

print("Testing /auth/token endpoint...")
try:
    # Try to access the token endpoint without authentication
    response = requests.post(
        f"{base_url}/auth/token",
        data={
            "username": "test@example.com",
            "password": "password"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting /auth/register endpoint...")
try:
    # Try to access the register endpoint without authentication
    response = requests.post(
        f"{base_url}/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting /health endpoint...")
try:
    # Test a public endpoint
    response = requests.get(f"{base_url}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")