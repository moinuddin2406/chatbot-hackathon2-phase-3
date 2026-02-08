import asyncio
import os
import sys
from sqlmodel import create_engine, Session

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Set environment variables to avoid config issues
os.environ.setdefault('DATABASE_URL', 'sqlite:///./todo_app.db')
os.environ.setdefault('COHERE_API_KEY', '')  # Empty key to force mock client

def test_chat_functionality():
    try:
        # Import the chat agent
        from chatbot.agents.chat_agent import chat_agent
        from chatbot.utils.validation import validate_user_exists
        
        print("[OK] Successfully imported chat agent")
        
        # Test the validation function
        result = validate_user_exists("testuser")
        print(f"[OK] validate_user_exists works: {result}")
        
        # Use the same database engine as the main app
        from db import engine
        
        async def run_test():
            # Test the chat agent process_message function
            # Use a session from the main app's engine
            with Session(engine) as db:
                result = await chat_agent.process_message(
                    user_id="testuser",
                    message="Hello, how are you?",
                    conversation_id=None,
                    db=db
                )
                print(f"[OK] Chat agent processed message successfully: {result}")
                return result
            
        # Run the async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_test())
        print(f"Final result: {result}")
        
    except Exception as e:
        print(f"[ERROR] Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_functionality()