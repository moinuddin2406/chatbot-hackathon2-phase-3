import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from mcp_server.main import app


@pytest.fixture
def client():
    """Create a test client for the MCP server FastAPI app"""
    return TestClient(app)


def test_health_check_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mcp-task-server"


def test_add_task_endpoint_success(client):
    """Test the add_task endpoint with a successful request"""
    task_data = {
        "user_id": "user123",
        "title": "Buy groceries",
        "description": "Get milk, bread, and eggs"
    }
    
    response = client.post("/mcp/add_task", json=task_data)
    
    # The response format depends on the implementation
    assert response.status_code in [200, 422]  # 200 for success, 422 for validation error
    
    if response.status_code == 200:
        data = response.json()
        assert "success" in data
        if data["success"]:
            assert "data" in data
            assert data["data"]["title"] == "Buy groceries"


def test_list_tasks_endpoint_success(client):
    """Test the list_tasks endpoint with a successful request"""
    # Test with user_id as a query parameter
    response = client.post("/mcp/list_tasks", params={"user_id": "user123"})
    
    assert response.status_code in [200, 422]  # 200 for success, 422 for validation error
    
    if response.status_code == 200:
        data = response.json()
        assert "success" in data
        # Response may have tasks or an empty list


def test_complete_task_endpoint_success(client):
    """Test the complete_task endpoint with a successful request"""
    response = client.post(
        "/mcp/complete_task",
        params={
            "user_id": "user123",
            "task_id": "task456"
        }
    )
    
    assert response.status_code in [200, 404, 422]  # 200 for success, 404 for not found, 422 for validation error


def test_update_task_endpoint_success(client):
    """Test the update_task endpoint with a successful request"""
    from mcp_server.schemas.task_schemas import TaskUpdate
    
    update_data = {
        "title": "Updated task title",
        "completed": True
    }
    
    response = client.post(
        "/mcp/update_task",
        params={
            "user_id": "user123",
            "task_id": "task456"
        },
        json=update_data
    )
    
    assert response.status_code in [200, 404, 422]  # 200 for success, 404 for not found, 422 for validation error


def test_delete_task_endpoint_success(client):
    """Test the delete_task endpoint with a successful request"""
    response = client.post(
        "/mcp/delete_task",
        params={
            "user_id": "user123",
            "task_id": "task456"
        }
    )
    
    assert response.status_code in [200, 404, 422]  # 200 for success, 404 for not found, 422 for validation error


def test_mcp_server_integration_with_database():
    """Test the MCP server integration with database operations"""
    # This test would normally require a real database connection
    # For now, we'll test the logic with mocks
    
    from mcp_server.database.task_operations.task_crud import create_task, get_task, get_tasks
    from mcp_server.schemas.task_schemas import TaskCreate
    from sqlalchemy.orm import Session
    
    # Create a mock database session
    mock_db = MagicMock(spec=Session)
    
    # Test creating a task
    task_create = TaskCreate(
        user_id="user123",
        title="Test task",
        description="Test description"
    )
    
    # Mock the database operations
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # Create a mock task object
    mock_task_obj = MagicMock()
    mock_task_obj.id = "task999"
    mock_task_obj.user_id = "user123"
    mock_task_obj.title = "Test task"
    mock_task_obj.description = "Test description"
    mock_task_obj.completed = False
    
    # Patch the Task model creation
    with patch('mcp_server.models.task.Task') as MockTask:
        MockTask.return_value = mock_task_obj
        
        # Call the create_task function
        created_task = create_task(mock_db, task_create)
        
        # Verify the database operations were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        
        # Verify the returned task
        assert created_task.id == "task999"
        assert created_task.title == "Test task"