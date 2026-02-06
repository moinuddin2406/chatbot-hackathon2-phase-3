import subprocess
import sys
import os

# Change to the backend directory
os.chdir(r"C:\Users\Moinuddin\Desktop\to-do-app_phase2\backend")

# Run the server with more verbose output
cmd = [
    sys.executable, "-c",
    """
import uvicorn
from main import app
import logging

# Enable logging
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

# Run the subprocess and capture output
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for a few seconds to see initial output
try:
    stdout, stderr = process.communicate(timeout=10)
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
except subprocess.TimeoutExpired:
    print("Server started successfully in the background")
    process.kill()