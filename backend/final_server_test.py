import requests
import time
import subprocess
import sys
import threading
import os

def start_server():
    """Function to start the server in a subprocess"""
    os.chdir(r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend")
    
    cmd = [
        sys.executable, "-c",
        """
import uvicorn
from main import app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn')

print('Starting server on http://127.0.0.1:8001')
print('Database initialization will happen on startup')

try:
    uvicorn.run(
        app, 
        host='127.0.0.1', 
        port=8001, 
        log_level='info',
        reload=False
    )
except Exception as e:
    print(f'Error starting server: {e}')
    import traceback
    traceback.print_exc()
"""
    ]
    
    # Start the server process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    # Print output from the server
    for line in iter(process.stdout.readline, ''):
        print(line.rstrip())
    
    process.wait()

def test_connection():
    """Function to test the connection once server is ready"""
    time.sleep(5)  # Wait for server to start
    
    url = "http://127.0.0.1:8001/health"
    try:
        response = requests.get(url, timeout=10)
        print(f"✓ Server is running!")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Server is not responding - connection error")
        return False
    except requests.exceptions.Timeout:
        print("✗ Server is not responding - timeout")
        return False
    except Exception as e:
        print(f"✗ Error testing server: {e}")
        return False

if __name__ == "__main__":
    print("Starting server in background...")
    
    # Start server in a thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a bit and then test connection
    time.sleep(10)
    success = test_connection()
    
    if not success:
        print("\nThe server may still be starting up. Please wait and try accessing:")
        print("- http://127.0.0.1:8001/health for health check")
        print("- http://127.0.0.1:8001/docs for API documentation")
    
    print("\nKeeping server running. Press Ctrl+C to stop.")
    try:
        server_thread.join()  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)