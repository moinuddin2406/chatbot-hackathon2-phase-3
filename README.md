# Phase 3 Chatbot - Full Stack Application

This is a full-stack Todo web application built with Next.js for the frontend and FastAPI for the backend. The application features user authentication, task management, and a responsive UI.

## Features

- User authentication (login/signup)
- Task management (create, read, update, delete)
- Responsive design for mobile, tablet, and desktop
- JWT-based authentication with secure session management
- Professional UI/UX design
- Separate backend API with FastAPI

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth
- React 18+

### Backend
- FastAPI
- Python
- SQLModel
- PostgreSQL (with Neon)

## Getting Started

### Prerequisites

Make sure you have Node.js and Python installed on your system.

### Frontend Setup

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Backend Setup

Navigate to the backend directory and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run the backend server:

```bash
uvicorn main:app --reload
```

## Project Structure

```text
.
├── app/                        # Next.js App Router pages
│   ├── login/                  # Login page
│   ├── signup/                 # Signup page
│   ├── dashboard/              # Dashboard page
│   ├── tasks/                  # Tasks page and sub-pages
│   │   ├── new/                # Create task page
│   │   └── [id]/               # Edit task page
│   └── layout.tsx              # Root layout
├── components/                 # Reusable UI components
│   ├── auth/                   # Authentication components
│   ├── tasks/                  # Task management components
│   ├── ui/                     # General UI components
│   └── navigation/             # Navigation components
├── context/                    # React context providers
│   └── auth-context.tsx        # Authentication state management
├── public/                     # Static assets
├── backend/                    # FastAPI backend application
│   ├── main.py                 # Main application entry point
│   ├── models/                 # Database models
│   ├── routes/                 # API routes
│   └── auth/                   # Authentication logic
├── frontend/                   # Frontend documentation and scripts
└── README.md                   # This file
```

## Environment Variables

Create a `.env.local` file in the root directory and add the following:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://www.better-auth.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)