# JWT-Protected Todo API Backend

This is the backend component of the JWT-Protected Todo API, built with Python, FastAPI, SQLModel, and PyJWT.

## Features

- JWT-based authentication and authorization
- Secure task management with user data isolation
- RESTful API endpoints for task operations
- Integration-ready with Next.js frontend using Better Auth

## Tech Stack

- Python 3.11+
- FastAPI - Modern, fast web framework
- SQLModel - SQL databases with Python objects
- PyJWT - JSON Web Token implementation
- Neon Serverless PostgreSQL - Cloud database
- Uvicorn - ASGI server

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the backend directory with the following variables:

```bash
BETTER_AUTH_SECRET=your_super_secret_key_here
BETTER_AUTH_URL=https://your-better-auth-domain.com
DATABASE_URL=postgresql://username:password@your-neon-db.neon.tech/dbname
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and environment variables
├── db.py                # Database connection and session management
├── models.py            # SQLModel database models
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # JWT authentication utilities
├── security.py          # Security utilities and user isolation
├── utils.py             # Utility functions and error handling
├── routes/              # API route definitions
│   └── tasks.py         # Task-related endpoints
└── services/            # Business logic services
    └── task_service.py  # Task management service
```