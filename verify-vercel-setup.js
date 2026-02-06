// Verification script to ensure the project is properly set up for Vercel deployment
const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying project setup for Vercel deployment...\n');

// Check for required files
const requiredFiles = [
  'package.json',
  'next.config.js',
  'vercel.json',
  'app/page.tsx'
];

let allGood = true;

for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ Found: ${file}`);
  } else {
    console.log(`❌ Missing: ${file}`);
    allGood = false;
  }
}

// Check package.json for Next.js dependency
if (allGood) {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  const hasNextInDeps = packageJson.dependencies && packageJson.dependencies.next;
  const hasNextInDevDeps = packageJson.devDependencies && packageJson.devDependencies.next;
  
  if (hasNextInDeps || hasNextInDevDeps) {
    console.log(`✅ Next.js found in ${hasNextInDeps ? 'dependencies' : 'devDependencies'}`);
  } else {
    console.log('❌ Next.js not found in package.json dependencies');
    allGood = false;
  }
}

// Check for duplicate app directories
const srcAppDir = path.join(__dirname, 'src', 'app');
if (fs.existsSync(srcAppDir)) {
  console.log('❌ Duplicate app directory still exists at src/app');
  allGood = false;
} else {
  console.log('✅ No duplicate app directory found');
}

// Check vercel.json configuration
if (allGood) {
  try {
    const vercelJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'vercel.json'), 'utf8'));
    const hasNextBuild = vercelJson.builds && vercelJson.builds.some(build => build.use === '@vercel/next');
    if (hasNextBuild) {
      console.log('✅ Vercel configuration is set up for Next.js');
    } else {
      console.log('❌ Vercel configuration does not include Next.js build');
      allGood = false;
    }
  } catch (e) {
    console.log('❌ Error reading vercel.json');
    allGood = false;
  }
}

console.log('\n' + '='.repeat(50));
if (allGood) {
  console.log('🎉 All checks passed! Your project should deploy successfully to Vercel.');
  console.log('\nTo deploy, make sure you have the Vercel CLI installed:');
  console.log('npm install -g vercel');
  console.log('\nThen run:');
  console.log('vercel --prod');
} else {
  console.log('⚠️  Some issues were found. Please fix them before deploying to Vercel.');
}
console.log('='.repeat(50));