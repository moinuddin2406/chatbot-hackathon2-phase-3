# Frontend UI with Authentication

This is the frontend for a multi-user Todo web application built with Next.js, TypeScript, Tailwind CSS, and Better Auth.

## Features

- User authentication (login/signup)
- Task management (create, read, update, delete)
- Responsive design for mobile, tablet, and desktop
- JWT-based authentication with secure session management
- Professional UI/UX design

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth
- React 18+

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Environment Variables

Create a `.env.local` file in the root of the `frontend` directory and add the following:

```env
NEXT_PUBLIC_API_BASE_URL=https://moinminhal-hack2-phase2.hf.space
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

For local development with a backend running on localhost, use:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Project Structure

```text
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── login/              # Login page
│   │   ├── signup/             # Signup page
│   │   ├── dashboard/          # Dashboard page
│   │   ├── tasks/              # Tasks page and sub-pages
│   │   │   ├── new/            # Create task page
│   │   │   └── [id]/           # Edit task page
│   │   └── layout.tsx          # Root layout
│   ├── components/             # Reusable UI components
│   │   ├── auth/               # Authentication components
│   │   ├── tasks/              # Task management components
│   │   ├── ui/                 # General UI components
│   │   └── navigation/         # Navigation components
│   ├── lib/                    # Utility functions and API client
│   │   ├── api.ts              # Centralized API client
│   │   ├── auth.ts             # Authentication utilities
│   │   └── types.ts            # TypeScript type definitions
│   ├── context/                # React context providers
│   │   └── auth-context.tsx    # Authentication state management
│   ├── styles/                 # Global styles
│   │   └── globals.css         # Tailwind and custom styles
│   └── hooks/                  # Custom React hooks
│       └── use-toast.ts        # Toast notification hook
├── public/                     # Static assets
└── tests/                      # Test files
```

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://www.better-auth.com/docs)