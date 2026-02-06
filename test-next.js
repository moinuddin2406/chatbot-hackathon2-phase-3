// Simple test to check if Next.js is working
console.log('Testing Next.js installation...');
const { exec } = require('child_process');

exec('npx next info', (error, stdout, stderr) => {
  console.log('Next.js Info:');
  console.log(stdout);
  if (error) {
    console.log('Error:', error.message);
  }
  if (stderr) {
    console.log('Stderr:', stderr);
  }
});