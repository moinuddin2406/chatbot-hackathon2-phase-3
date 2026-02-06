import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test basic imports
    import fastapi
    import uvicorn
    print(f"FastAPI version: {fastapi.__version__}")
    print(f"Uvicorn version: {uvicorn.__version__}")
    
    # Test importing our app
    from main import app
    print("✓ Successfully imported main app")
    
    # Test importing other components
    from config import settings
    print("✓ Successfully imported config")
    
    from db import create_db_and_tables
    print("✓ Successfully imported db functions")
    
    print("\nAll imports successful! The server should be able to start.")
    
    # Try to initialize the database
    print("\nTrying to initialize database...")
    create_db_and_tables()
    print("✓ Database initialized successfully")
    
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()