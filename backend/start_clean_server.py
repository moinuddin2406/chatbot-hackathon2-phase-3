import sys
import os
import subprocess

# Change to backend directory
os.chdir(r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend")

# Check if there are any existing processes using port 8001
print("Checking for processes on port 8001...")
result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)

for line in result.stdout.splitlines():
    if ':8001' in line and 'LISTENING' in line:
        print(f"Found process using port 8001: {line}")
        # Extract PID and kill the process
        parts = line.split()
        if len(parts) > 4:
            pid = parts[4]
            print(f"Killing process {pid}...")
            subprocess.run(['taskkill', '/F', '/PID', pid])

print("Port 8001 should now be free.")

# Now try to start the server
cmd = [
    sys.executable, "-c",
    """
import uvicorn
from main import app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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

print("Starting server...")
subprocess.run(cmd)