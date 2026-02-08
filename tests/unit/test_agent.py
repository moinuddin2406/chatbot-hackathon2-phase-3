import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.chatbot.agents.chat_agent import ChatAgent
from backend.chatbot.agents.intent_detector import IntentDetector
from backend.chatbot.agents.tool_router import ToolRouter
from backend.chatbot.agents.response_generator import ResponseGenerator


@pytest.fixture
def mock_db():
    """Mock database session for testing"""
    db = MagicMock()
    return db


@pytest.mark.asyncio
async def test_chat_agent_process_message():
    """Test the chat agent's process_message method"""
    agent = ChatAgent()
    
    # Mock the dependencies
    with patch.object(agent.cohere_client, 'chat_with_tools') as mock_cohere, \
         patch.object(agent.mcp_client, 'add_task') as mock_add_task:
        
        # Mock Cohere response
        mock_cohere.return_value = {
            "text": "I've added your task.",
            "tool_calls": [
                {
                    "name": "add_task",
                    "parameters": {"title": "Buy milk", "description": "Get 2% milk from store"}
                }
            ]
        }
        
        # Mock MCP client response
        mock_add_task.return_value = {
            "success": True,
            "data": {"task_id": "task123", "title": "Buy milk", "completed": False}
        }
        
        # Call the method
        result = await agent.process_message(
            user_id="user123",
            message="Add a task to buy milk",
            conversation_id=None,
            db=MagicMock()
        )
        
        # Verify the result
        assert result["response"] == "I've added your task."
        assert result["conversation_id"] is not None
        assert result["tool_calls"] is not None


def test_intent_detector_detect_intent():
    """Test the intent detector's detect_intent method"""
    detector = IntentDetector()
    
    # Test different intents
    assert detector.detect_intent("Add a task to buy milk") == "add_task"
    assert detector.detect_intent("Show me my tasks") == "list_tasks"
    assert detector.detect_intent("Complete task 1") == "complete_task"
    assert detector.detect_intent("Update task 1 to be more important") == "update_task"
    assert detector.detect_intent("Delete task 1") == "delete_task"
    assert detector.detect_intent("Hello there") == "general_query"


def test_intent_detector_extract_task_details():
    """Test the intent detector's extract_task_details method"""
    detector = IntentDetector()
    
    # Test extracting task details from a message
    message = "Add a task to buy milk from the store"
    details = detector.extract_task_details(message)
    
    assert "buy milk" in details["title"] or "buy milk from the store" == details["title"]
    assert details["description"] == ""  # Our simple implementation doesn't extract descriptions


def test_response_generator_generate_response():
    """Test the response generator's generate_response method"""
    generator = ResponseGenerator()
    
    # Test generating a response for adding a task
    tool_result = {
        "success": True,
        "data": {"title": "Buy milk", "task_id": "task123"}
    }
    
    response = generator.generate_response("add_task", tool_result, "Add a task to buy milk")
    
    assert "Buy milk" in response
    assert "added" in response.lower()


def test_response_generator_generate_error_response():
    """Test the response generator's error response generation"""
    generator = ResponseGenerator()
    
    # Test generating an error response
    tool_result = {
        "success": False,
        "error": {"code": "TASK_NOT_FOUND", "message": "Task not found"}
    }
    
    response = generator.generate_response("complete_task", tool_result, "Complete task 1")
    
    assert "couldn't find" in response.lower() or "task not found" in response.lower()


@pytest.mark.asyncio
async def test_tool_router_route_intent():
    """Test the tool router's route_intent method"""
    router = ToolRouter()
    
    # Mock the MCP client
    with patch.object(router.mcp_client, 'add_task') as mock_add_task:
        mock_add_task.return_value = {
            "success": True,
            "data": {"task_id": "task123", "title": "Buy milk", "completed": False}
        }
        
        # Test routing an add_task intent
        result = await router.route_intent(
            user_id="user123",
            message="Add a task to buy milk",
            conversation_context=None
        )
        
        # Verify the result
        assert result["success"] is True
        assert result["data"]["title"] == "Buy milk"
        
        # Verify the MCP client was called
        mock_add_task.assert_called_once()