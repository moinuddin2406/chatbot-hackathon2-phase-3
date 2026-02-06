import uvicorn
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

if __name__ == '__main__':
    print("Starting server on http://127.0.0.1:8001")
    print("Database initialization will happen on startup")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001, 
        log_level="debug",  # More verbose logging
        reload=False
    )