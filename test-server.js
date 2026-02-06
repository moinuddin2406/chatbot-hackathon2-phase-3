// This is a simple test to check if Next.js is working properly
const { spawn } = require('child_process');

console.log('Attempting to run Next.js dev server...');

const devServer = spawn('npx', ['next', 'dev'], {
  cwd: './frontend',
  stdio: 'pipe',
  shell: true
});

devServer.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

devServer.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

devServer.on('close', (code) => {
  console.log(`Child process exited with code ${code}`);
});