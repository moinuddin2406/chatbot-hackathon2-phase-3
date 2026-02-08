from fastapi import FastAPI
from .logging_config import setup_logging
from .config import settings
from .routes.task_routes import router as task_router


def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(
        title="MCP Task Server API",
        description="MCP server for task operations in the AI-powered Todo Chatbot",
        version="1.0.0"
    )
    
    # Include the task routes
    app.include_router(task_router, prefix="/mcp", tags=["tasks"])
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "mcp-task-server"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Default port for MCP server
        reload=True
    )