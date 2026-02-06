import subprocess
import sys
import os
import time
import requests
import threading

def diagnose_backend():
    print("Diagnosing backend loading issues...")
    
    # Change to backend directory
    backend_dir = r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend"
    os.chdir(backend_dir)
    print(f"Changed to directory: {backend_dir}")
    
    # Check Python installation
    print("\n1. Checking Python installation...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"Python version: {result.stdout.strip()}")
    except Exception as e:
        print(f"Error checking Python: {e}")
        return
    
    # Check required packages
    print("\n2. Checking required packages...")
    required_packages = ["fastapi", "uvicorn", "sqlmodel", "pyjwt", "passlib"]
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                print(f"✓ {package} installed successfully")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
    
    # Test imports
    print("\n3. Testing imports...")
    try:
        import fastapi
        import uvicorn
        from main import app
        from config import settings
        from db import create_db_and_tables
        print("✓ All imports successful")
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Create database tables
    print("\n4. Creating database tables...")
    try:
        create_db_and_tables()
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Start server in a thread
    print("\n5. Starting server in background...")
    def start_server():
        try:
            import uvicorn
            from main import app
            uvicorn.run(app, host='127.0.0.1', port=8001, log_level='warning', reload=False)
        except Exception as e:
            print(f"Server startup error: {e}")
            import traceback
            traceback.print_exc()
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting 10 seconds for server to start...")
    time.sleep(10)
    
    # Test server connection
    print("\n6. Testing server connection...")
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=10)
        if response.status_code == 200:
            print(f"✓ Server is responding! Status: {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print(f"✗ Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Server is not responding - connection error")
    except requests.exceptions.Timeout:
        print("✗ Server is not responding - timeout")
    except Exception as e:
        print(f"✗ Error testing server: {e}")
    
    print("\nDiagnostic complete.")
    print("Press Ctrl+C to stop the server.")

if __name__ == "__main__":
    diagnose_backend()
    
    # Keep the script running so the server stays up
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")