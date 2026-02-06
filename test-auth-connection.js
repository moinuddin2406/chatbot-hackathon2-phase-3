// Simple test to verify the authentication endpoints are accessible
const API_BASE_URL = 'http://localhost:8000';

async function testAuthEndpoints() {
  console.log('Testing authentication endpoints...\n');
  
  // Test health endpoint
  try {
    const healthResponse = await fetch(`${API_BASE_URL}/health`);
    const healthData = await healthResponse.json();
    console.log('✓ Health check:', healthData);
  } catch (error) {
    console.error('✗ Health check failed:', error.message);
  }
  
  // Test register endpoint with a test request
  try {
    const registerResponse = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: 'Test User',
        email: 'test-connection@example.com',
        password: 'password123'
      })
    });
    
    if (registerResponse.status === 400) { // User already exists
      const data = await registerResponse.json();
      console.log('✓ Register endpoint accessible (user already exists):', data.detail);
    } else if (registerResponse.ok) {
      const data = await registerResponse.json();
      console.log('✓ Register endpoint working:', data);
    } else {
      const data = await registerResponse.json().catch(() => ({}));
      console.error('✗ Register endpoint error:', data.detail || registerResponse.status);
    }
  } catch (error) {
    console.error('✗ Register endpoint failed:', error.message);
  }
  
  // Test token endpoint with a test request
  try {
    const tokenResponse = await fetch(`${API_BASE_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'username=test-connection@example.com&password=password123'
    });
    
    if (tokenResponse.status === 401) { // Invalid credentials
      console.log('✓ Token endpoint accessible (invalid credentials): 401 Unauthorized');
    } else if (tokenResponse.ok) {
      const data = await tokenResponse.json();
      console.log('✓ Token endpoint working:', Object.keys(data));
    } else {
      const data = await tokenResponse.json().catch(() => ({}));
      console.error('✗ Token endpoint error:', data.detail || tokenResponse.status);
    }
  } catch (error) {
    console.error('✗ Token endpoint failed:', error.message);
  }
  
  console.log('\nTest completed.');
}

// Run the test
testAuthEndpoints();