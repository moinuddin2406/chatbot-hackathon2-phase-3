import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test importing the chat agent directly
try:
    from chatbot.agents.chat_agent import chat_agent
    print("Chat agent imported successfully")
    
    # Test the process_message function directly
    import asyncio
    from sqlmodel import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Use the same database as the main app
    DATABASE_URL = "sqlite:///./todo_app.db"  # Adjust as needed
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    async def test_chat():
        db = SessionLocal()
        try:
            result = await chat_agent.process_message(
                user_id="testuser",
                message="Say hello",
                conversation_id=None,
                db=db
            )
            print("Chat result:", result)
        except Exception as e:
            print("Error in chat processing:", str(e))
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    
    asyncio.run(test_chat())
    
except Exception as e:
    print("Error importing or running chat agent:", str(e))
    import traceback
    traceback.print_exc()