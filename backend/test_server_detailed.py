import sys
import threading
import time
import requests
from main import app
import uvicorn

def run_server():
    """Run the server in a separate thread"""
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="debug")
    server = uvicorn.Server(config)
    server.run()

def test_server():
    """Test the server after a delay"""
    time.sleep(3)  # Wait for server to start
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test the server
    test_server()
    
    # Keep the main thread alive for a bit to see server logs
    time.sleep(10)