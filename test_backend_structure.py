"""
Basic test to verify the JWT-Protected Todo API backend structure
"""
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_backend_structure():
    """Test that all required modules can be imported without errors"""
    try:
        # Test importing the main application
        from backend.main import app
        assert app is not None
        print("✓ Main application imported successfully")
        
        # Test importing configuration
        from backend.config import settings
        assert settings is not None
        print("✓ Configuration imported successfully")
        
        # Test importing database module
        from backend.db import engine, get_session
        assert engine is not None
        assert get_session is not None
        print("✓ Database module imported successfully")
        
        # Test importing models
        from backend.models import Task, TaskCreate, TaskUpdate
        assert Task is not None
        assert TaskCreate is not None
        assert TaskUpdate is not None
        print("✓ Models imported successfully")
        
        # Test importing authentication
        from backend.auth import get_current_user, verify_token
        assert get_current_user is not None
        assert verify_token is not None
        print("✓ Authentication module imported successfully")
        
        # Test importing security
        from backend.security import check_user_id_match, verify_user_owns_resource
        assert check_user_id_match is not None
        assert verify_user_owns_resource is not None
        print("✓ Security module imported successfully")
        
        # Test importing utilities
        from backend.utils import handle_error, log_api_call, APIError
        assert handle_error is not None
        assert log_api_call is not None
        assert APIError is not None
        print("✓ Utilities module imported successfully")
        
        # Test importing services
        from backend.services.task_service import TaskService
        assert TaskService is not None
        print("✓ Task service imported successfully")
        
        # Test importing routes
        from backend.routes.tasks import router
        assert router is not None
        print("✓ Task routes imported successfully")
        
        print("\n🎉 All modules imported successfully!")
        print("The backend structure is properly implemented.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend_structure()
    if not success:
        sys.exit(1)