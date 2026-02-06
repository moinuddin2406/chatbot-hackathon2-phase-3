import subprocess
import time
import requests
import sys
import threading

def start_server():
    """Start the server in a subprocess"""
    cmd = [sys.executable, "-c", """
import uvicorn
from main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info')
"""]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend")
    return process

def test_server():
    """Test if the server is running"""
    url = "http://127.0.0.1:8001/health"
    
    # Give the server some time to start
    time.sleep(5)
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Server is running!")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not responding - connection error")
        return False
    except requests.exceptions.Timeout:
        print("Server is not responding - timeout")
        return False
    except Exception as e:
        print(f"Error testing server: {e}")
        return False

if __name__ == "__main__":
    print("Starting server...")
    server_process = start_server()
    
    print("Testing server...")
    is_running = test_server()
    
    if not is_running:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")
    else:
        print("Server is working correctly. Press Ctrl+C to stop.")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\nTerminating server...")
            server_process.terminate()
            server_process.wait()