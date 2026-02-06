import subprocess
import sys
import time
import requests
import threading
import os

def run_server():
    """Function to run the server"""
    os.chdir(r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend")
    
    cmd = [
        sys.executable, "-c",
        """
import uvicorn
import logging
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Starting server on http://127.0.0.1:8000")
print("Using SQLite database configuration")
print("")

try:
    # Create database tables first
    from db import create_db_and_tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully.")
    
    print("Starting server...")
    uvicorn.run(
        app, 
        host='127.0.0.1', 
        port=8000, 
        log_level='info',
        reload=False,
        timeout_keep_alive=30
    )
except Exception as e:
    print(f'Error starting server: {e}')
    import traceback
    traceback.print_exc()
"""
    ]
    
    # Start the server process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
    
    # Print output from the server in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"[SERVER] {output.strip()}")
    
    process.wait()

def test_server():
    """Function to test the server after it starts"""
    time.sleep(8)  # Wait for server to start
    
    print("\\nTesting server connection...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=10)
        print(f"✓ Server responded with status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test auth endpoints
        try:
            auth_response = requests.get("http://127.0.0.1:8000/docs", timeout=10)
            print(f"✓ API docs available with status: {auth_response.status_code}")
        except:
            print("✗ Could not reach API docs")
            
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Server is not responding: {e}")
        return False

if __name__ == "__main__":
    print("Starting server in background...")
    
    # Start server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a bit and then test connection
    time.sleep(3)
    success = test_server()
    
    if not success:
        print("\\nTrying alternative addresses...")
        try:
            # Try localhost
            response = requests.get("http://localhost:8000/health", timeout=10)
            print(f"✓ Server responded on localhost with status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Server not responding on localhost either: {e}")
    
    print("\\nServer running. Press Ctrl+C to stop.")
    try:
        server_thread.join()  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\\nStopping server...")
        sys.exit(0)