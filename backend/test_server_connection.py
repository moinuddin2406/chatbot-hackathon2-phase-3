import subprocess
import sys
import time
import threading
import requests
import socket

def check_port(host, port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((host, port))
        return result == 0  # 0 means connection successful (port in use)

def run_server():
    """Run the minimal server"""
    cmd = [
        sys.executable, "-c",
        """
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting minimal server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
"""
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print output from the server
    for line in iter(process.stdout.readline, ''):
        print(f"SERVER: {line.rstrip()}")
    
    process.wait()

def test_server():
    """Test the server after it starts"""
    time.sleep(5)  # Wait for server to start
    
    print("Testing server connection...")
    
    # Check if port is in use
    if check_port('127.0.0.1', 8001):
        print("✓ Port 8001 is in use")
        
        # Try to make a request
        try:
            response = requests.get("http://127.0.0.1:8001/health", timeout=10)
            print(f"✓ Server responded with status: {response.status_code}")
            print(f"Response: {response.json()}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return False
    else:
        print("✗ Port 8001 is not in use - server may not have started")
        return False

if __name__ == "__main__":
    print("Starting server in background...")
    
    # Start server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a bit and then test
    success = test_server()
    
    if not success:
        print("\nTrying alternative approach...")
        # Try with localhost instead of 127.0.0.1
        time.sleep(2)
        try:
            response = requests.get("http://localhost:8001/health", timeout=10)
            print(f"✓ Server responded on localhost with status: {response.status_code}")
            print(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Request to localhost also failed: {e}")
    
    print("\nKeeping server running. Press Ctrl+C to stop.")
    try:
        server_thread.join()  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)