# Simple test to check if there are any import errors
try:
    print("Testing imports...")
    from main import app
    print("✓ Main app imported successfully")
    
    from config import settings
    print("✓ Config settings imported successfully")
    
    from db import create_db_and_tables
    print("✓ DB functions imported successfully")
    
    from auth import create_access_token, verify_token, get_current_user
    print("✓ Auth functions imported successfully")
    
    from routes.auth import router as auth_router
    print("✓ Auth routes imported successfully")
    
    from routes.tasks import router as task_router
    print("✓ Task routes imported successfully")
    
    print("\nAll imports successful! The backend should work properly.")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")