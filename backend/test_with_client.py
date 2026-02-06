import sys
import os
import logging

# Set up logging to see detailed information
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Setting up the application...")

try:
    from main import app
    print("Application imported successfully")
    
    # Test creating a test client
    from fastapi.testclient import TestClient
    client = TestClient(app)
    print("Test client created successfully")
    
    # Test the root endpoint
    print("Testing root endpoint...")
    response = client.get("/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test the health endpoint
    print("Testing health endpoint...")
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    print("Basic tests completed successfully!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()