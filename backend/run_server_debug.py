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
        timeout_keep_alive=120
    )
except KeyboardInterrupt:
    print('Server stopped by user')
except Exception as e:
    print(f'Error starting server: {e}')
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")