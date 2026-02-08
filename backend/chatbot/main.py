from fastapi import FastAPI
from .logging_config import setup_logging
from .config import settings


def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(
        title="AI-Powered Todo Chatbot API",
        description="API for the AI-powered Todo Chatbot that integrates with an existing full-stack application",
        version="1.0.0"
    )
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "chatbot-api"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )