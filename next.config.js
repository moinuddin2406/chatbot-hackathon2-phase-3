/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  reactCompiler: false, // Disable reactCompiler to avoid Turbopack issues in some environments
  // Other configuration options can be added here
  experimental: {
    // Other experimental features can be added here
  },
  // Configure redirects or rewrites if needed
  async redirects() {
    return [
      // Example redirect configuration
      // {
      //   source: '/old-url',
      //   destination: '/new-url',
      //   permanent: true,
      // },
    ];
  },
  async rewrites() {
    // Determine the backend URL based on environment
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

    return [
      // Proxy API requests to the backend
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
      // Proxy auth requests to the backend
      {
        source: '/auth/:path*',
        destination: `${backendUrl}/auth/:path*`,
      },
    ]
  },
};

module.exports = nextConfig;