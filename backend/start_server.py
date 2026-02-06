#!/usr/bin/env python
"""
Startup script for the JWT-Protected Todo API
This script ensures the database is initialized before starting the server
"""

import sys
import os
import threading
import time
from db import create_db_and_tables

def init_database():
    """Initialize the database tables"""
    print("Initializing database tables...")
    try:
        create_db_and_tables()
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    import uvicorn
    from main import app
    
    print("Starting server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info", reload=False)

if __name__ == "__main__":
    # Initialize the database first
    if not init_database():
        print("Failed to initialize database. Exiting.")
        sys.exit(1)
    
    # Start the server
    start_server()