# Project Structure

This project follows a monorepo structure with both frontend and backend code in the same repository.

## Frontend

The frontend is built with Next.js and follows these conventions:

- `app/` - Main application pages using the App Router
- `components/` - Reusable UI components
- `context/` - React context providers
- `public/` - Static assets
- Root-level configuration files (next.config.js, tsconfig.json, package.json, etc.)

## Backend

The backend is located in the `backend/` directory and includes:

- FastAPI application
- Database models and schemas
- API routes
- Authentication logic

## Running the Application

### Frontend Development

From the root directory:

```bash
npm run dev
```

### Backend Development

From the backend directory:

```bash
cd backend
uvicorn main:app --reload
```

## Environment Variables

Both frontend and backend share some environment variables, which are typically defined in a `.env` file in the root directory.