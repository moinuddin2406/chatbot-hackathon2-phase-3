import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from backend.chatbot.main import app
from backend.chatbot.agents.chat_agent import chat_agent


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_chat_endpoint_success(client):
    """Test the chat endpoint with a successful request"""
    # Mock the chat agent's process_message method
    with patch.object(chat_agent, 'process_message') as mock_process:
        mock_process.return_value = {
            "conversation_id": "test_conv_123",
            "response": "I've added your task to buy milk.",
            "tool_calls": []
        }
        
        # Make a request to the chat endpoint
        response = client.post(
            "/api/user123/chat",
            json={"message": "Add a task to buy milk"}
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == "test_conv_123"
        assert "buy milk" in data["response"]


@pytest.mark.asyncio
async def test_chat_endpoint_missing_message(client):
    """Test the chat endpoint with a missing message"""
    response = client.post(
        "/api/user123/chat",
        json={}  # Missing message field
    )
    
    # Should return a validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_endpoint_empty_message(client):
    """Test the chat endpoint with an empty message"""
    response = client.post(
        "/api/user123/chat",
        json={"message": ""}
    )
    
    # Should return a validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_endpoint_with_conversation_id(client):
    """Test the chat endpoint with an existing conversation ID"""
    # Mock the chat agent's process_message method
    with patch.object(chat_agent, 'process_message') as mock_process:
        mock_process.return_value = {
            "conversation_id": "existing_conv_456",
            "response": "I've added another task.",
            "tool_calls": []
        }
        
        # Make a request to the chat endpoint with a conversation ID
        response = client.post(
            "/api/user123/chat",
            json={
                "conversation_id": "existing_conv_456",
                "message": "Add another task"
            }
        )
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == "existing_conv_456"
        assert "another task" in data["response"]


@pytest.mark.asyncio
async def test_chat_agent_integration():
    """Test the chat agent integration with mocked external services"""
    # This test simulates the integration between the chat agent and external services
    # without actually calling them
    
    # Mock the Cohere client and MCP client
    with patch('backend.chatbot.agents.chat_agent.cohere_client') as mock_cohere, \
         patch('backend.chatbot.agents.chat_agent.mcp_client') as mock_mcp:
        
        # Mock Cohere response
        mock_cohere.chat_with_tools.return_value = {
            "text": "I will add your task.",
            "tool_calls": [
                {
                    "name": "add_task",
                    "parameters": {"title": "Buy bread", "description": "Get sourdough bread"}
                }
            ]
        }
        
        # Mock MCP client response
        mock_mcp.add_task = AsyncMock(return_value={
            "success": True,
            "data": {"task_id": "task789", "title": "Buy bread", "completed": False}
        })
        
        # Mock the process_tool_results method
        mock_cohere.process_tool_results.return_value = "I've added the task 'Buy bread' to your list."
        
        # Create a mock database session
        mock_db = AsyncMock()
        
        # Call the chat agent's process_message method
        result = await chat_agent.process_message(
            user_id="user456",
            message="Add a task to buy bread",
            conversation_id=None,
            db=mock_db
        )
        
        # Verify the results
        assert result["response"] == "I've added the task 'Buy bread' to your list."
        assert result["conversation_id"] is not None
        assert result["tool_calls"] is not None
        
        # Verify that the external services were called
        mock_cohere.chat_with_tools.assert_called_once()
        mock_mcp.add_task.assert_called_once()
        mock_cohere.process_tool_results.assert_called_once()