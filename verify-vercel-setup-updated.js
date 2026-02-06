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
  
  // Check React/React DOM versions compatibility
  const hasReact = packageJson.dependencies && packageJson.dependencies.react;
  const hasReactDOM = packageJson.dependencies && packageJson.dependencies['react-dom'];

  if (hasReact && hasReactDOM) {
    console.log('✅ React and React DOM found in dependencies');

    // Check if versions are compatible with Next.js 14
    if (hasReact.includes('^18') && hasReactDOM.includes('^18')) {
      console.log('✅ React and React DOM versions are compatible with Next.js 14');
    } else if (hasReact.includes('19')) {
      console.log('⚠️  Warning: React 19 may not be fully compatible with Next.js 14');
      allGood = false;
    }
  } else {
    console.log('❌ React or React DOM not found in dependencies');
    allGood = false;
  }

  // Check Node.js engine version
  if (packageJson.engines && packageJson.engines.node) {
    if (packageJson.engines.node.includes('24.x')) {
      console.log('✅ Node.js engine version is compatible with Vercel');
    } else {
      console.log('⚠️  Node.js engine version might not be optimal for Vercel');
    }
  } else {
    console.log('⚠️  Node.js engine version not specified in package.json');
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
// For Next.js projects, Vercel supports zero config, so an empty config is fine
if (allGood) {
  try {
    const vercelJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'vercel.json'), 'utf8'));
    // If there are no custom builds, it's using zero config which is fine for Next.js
    if (!vercelJson.builds) {
      console.log('✅ Vercel configuration using zero-config (recommended for Next.js)');
    } else {
      const hasNextBuild = vercelJson.builds && vercelJson.builds.some(build => build.use === '@vercel/next');
      if (hasNextBuild) {
        console.log('✅ Vercel configuration is set up for Next.js');
      } else {
        console.log('❌ Vercel configuration does not include Next.js build');
        allGood = false;
      }
    }
  } catch (e) {
    console.log('❌ Error reading vercel.json');
    allGood = false;
  }
}

console.log('\n' + '='.repeat(70));
if (allGood) {
  console.log('🎉 All checks passed! Your project should deploy successfully to Vercel.');
  console.log('\nKey changes made:');
  console.log('- Downgraded React and React DOM to v18 (compatible with Next.js 14)');
  console.log('- Set Node.js engine to 24.x (compatible with Vercel)');
  console.log('- Simplified vercel.json to use zero-configuration');
  console.log('- Removed duplicate app directory');
  console.log('\nTo deploy, make sure you have the Vercel CLI installed:');
  console.log('npm install -g vercel');
  console.log('\nThen run:');
  console.log('vercel --prod');
} else {
  console.log('⚠️  Some issues were found. Please fix them before deploying to Vercel.');
}
console.log('='.repeat(70));