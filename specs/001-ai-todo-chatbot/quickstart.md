# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides instructions for setting up and running the AI-powered Todo Chatbot locally. The system consists of a frontend UI, a FastAPI backend with AI agent capabilities, and an MCP tool server.

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- Access to Cohere API key
- PostgreSQL database (or SQLite for development)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=<your-cohere-api-key>
DATABASE_URL=postgresql://user:password@localhost/dbname  # or sqlite:///./chatbot.db for SQLite
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MCP_SERVER_URL=http://localhost:8001  # URL for MCP tool server
```

#### Run Database Migrations
```bash
alembic upgrade head
```

#### Start the Backend Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. MCP Tool Server Setup

#### Navigate to MCP Server Directory
```bash
cd mcp-server  # or wherever your MCP server is located
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the MCP server directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname  # or sqlite:///./chatbot.db for SQLite
SECRET_KEY=<your-secret-key>
```

#### Start the MCP Server
```bash
uvicorn main:app --reload --port 8001
```

### 4. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend  # or the root directory if using Next.js
```

#### Install Dependencies
```bash
npm install
```

#### Set Up Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_COHERE_API_KEY=<your-cohere-api-key>
```

#### Start the Frontend Development Server
```bash
npm run dev
```

## Verification

1. Visit `http://localhost:3000` in your browser
2. You should see the main application with a floating chatbot icon
3. Click the chatbot icon to open the chat panel
4. Try sending a message like "Add a task to buy milk"
5. The AI should respond and create the task

## Troubleshooting

### Common Issues

#### Issue: Cannot connect to database
**Solution**: Verify your DATABASE_URL is correct and the database server is running

#### Issue: Cohere API returns authentication error
**Solution**: Check that your COHERE_API_KEY is set correctly in both backend and frontend

#### Issue: MCP server not responding
**Solution**: Verify the MCP_SERVER_URL in your backend .env file matches the actual MCP server URL

#### Issue: Chatbot UI not appearing
**Solution**: Check browser console for JavaScript errors and verify frontend is running on port 3000

## Next Steps

1. Customize the chatbot's personality by modifying the system prompt
2. Add more tools to the MCP server for extended functionality
3. Implement additional UI customization options
4. Set up production deployment configurations