import uvicorn
import sys
import traceback
from main import app

def run_server():
    try:
        print("Starting server on http://127.0.0.1:8001")
        print("Database initialization will happen on startup")
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8001, 
            log_level="info",
            reload=False
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run_server()