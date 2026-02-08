# Frontend

This is the frontend portion of the application built with Next.js. The frontend code is structured according to Next.js 13+ App Router conventions.

## Structure

The frontend code is organized as follows:

- `app/` - Contains the main application pages and API routes using the App Router
- `components/` - Reusable UI components organized by functionality
- `context/` - React context providers for state management
- `public/` - Static assets like images and icons

## Development

To run the frontend in development mode:

```bash
npm run dev
```

## Building

To build the frontend for production:

```bash
npm run build
```

## Starting the Server

To start the production server:

```bash
npm run start
```

## Environment Variables

The frontend requires the following environment variables:

- `NEXT_PUBLIC_API_BASE_URL` - The URL of the backend API server
- `BACKEND_URL` - Alternative variable for the backend URL

## Technologies Used

- Next.js 14+
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth for authentication