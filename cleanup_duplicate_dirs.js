// Script to remove duplicate src/app directory
// Run this script to clean up the duplicate directory that was causing Vercel deployment issues

const fs = require('fs');
const path = require('path');

// Define the paths
const duplicateDir = path.join(__dirname, 'src', 'app');
const mainAppDir = path.join(__dirname, 'app');

console.log('Checking for duplicate app directory at:', duplicateDir);

// Check if the duplicate directory exists
if (fs.existsSync(duplicateDir)) {
    console.log('Duplicate app directory found. Removing it...');
    
    // Remove the duplicate directory recursively
    const { execSync } = require('child_process');
    
    try {
        // Using rimraf for reliable directory removal
        execSync('npx rimraf "' + duplicateDir + '"', { stdio: 'inherit' });
        console.log('Successfully removed duplicate src/app directory.');
        console.log('Vercel deployment issue should now be resolved.');
    } catch (error) {
        console.error('Error removing duplicate directory:', error.message);
        console.log('Try running: npx rimraf "src/app" manually');
    }
} else {
    console.log('Duplicate app directory not found.');
}

console.log('\nThe main app directory at', mainAppDir, 'will continue to be used by Next.js.');
console.log('Your Vercel deployment should now work correctly.');