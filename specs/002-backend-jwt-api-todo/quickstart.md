# Quickstart Guide: JWT-Protected REST API for Todo Application

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL
- Better Auth service running

## Environment Setup

Create a `.env` file with the following variables:

```bash
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=https://your-better-auth-domain.com
DATABASE_URL=postgresql://username:password@your-neon-db.neon.tech/dbname
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel pyjwt python-multipart
```

## Running the Application

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

## API Usage

### Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

### Available Endpoints

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

### Example Request

```bash
curl -X GET \
  http://localhost:8000/api/user123/tasks \
  -H 'Authorization: Bearer your_jwt_token_here'
```

## Testing

Run the tests with pytest:

```bash
pytest
```

## Deployment

1. Ensure all environment variables are set in your deployment environment
2. Deploy to your preferred hosting platform (Heroku, AWS, etc.)
3. Verify the application is running and accessible