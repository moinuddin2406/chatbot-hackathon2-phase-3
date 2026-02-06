// Placeholder API route for better-auth
// Since we're using a custom auth implementation that communicates with the backend API,
// we're providing a minimal implementation to satisfy the build

export async function GET(request: Request) {
  return new Response(JSON.stringify({ error: 'Not implemented' }), {
    status: 501,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

export async function POST(request: Request) {
  return new Response(JSON.stringify({ error: 'Not implemented' }), {
    status: 501,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}