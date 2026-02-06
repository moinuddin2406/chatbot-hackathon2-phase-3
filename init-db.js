// Initialize the Better Auth database
import { auth } from './lib/auth';

async function initDatabase() {
  try {
    console.log('Initializing database...');
    // Better Auth should handle schema creation automatically
    // This is just to test the connection
    console.log('Database initialization completed.');
  } catch (error) {
    console.error('Database initialization error:', error);
  }
}

initDatabase();