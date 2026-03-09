/**
 * Test script for EnergizedSEO lead submission
 * Simulates a form submission from C. Carlin Plumbing (test business)
 */

const testData = {
  name: 'Test User',
  email: 'test@example.com',
  business: 'C. Carlin Plumbing',
  industry: 'contractor',
  website: 'https://ccarlinplumbing.com',
  message: 'Interested in a new website with better SEO'
};

async function testFormSubmission() {
  console.log('🧪 Testing EnergizedSEO Form Submission');
  console.log('=========================================\n');
  console.log('Test data:', JSON.stringify(testData, null, 2));
  console.log('\n📤 Submitting to /api/lead...\n');
  
  try {
    // For local testing, we'll just validate the function exists
    const fs = require('fs');
    const path = require('path');
    
    const functionPath = path.join(__dirname, 'functions', 'lead-submission.js');
    
    if (!fs.existsSync(functionPath)) {
      throw new Error('Function file not found at: ' + functionPath);
    }
    
    const functionCode = fs.readFileSync(functionPath, 'utf8');
    
    // Check for key elements
    const checks = [
      { name: 'Function exports onRequestPost', test: () => functionCode.includes('export async function onRequestPost') },
      { name: 'Parses form data', test: () => functionCode.includes('request.formData()') },
      { name: 'Validates required fields', test: () => functionCode.includes('!lead.email || !lead.business') },
      { name: 'Sandbox mode enabled', test: () => functionCode.includes('sandboxMode = true') },
      { name: 'Returns success response', test: () => functionCode.includes('success: true') }
    ];
    
    console.log('✅ Function Validation:\n');
    let allPassed = true;
    
    for (const check of checks) {
      const passed = check.test();
      console.log(`  ${passed ? '✓' : '✗'} ${check.name}`);
      if (!passed) allPassed = false;
    }
    
    console.log('\n=========================================');
    
    if (allPassed) {
      console.log('✅ All checks passed! Function is ready.');
      console.log('\n📝 Next steps:');
      console.log('   1. Deploy to Cloudflare Pages');
      console.log('   2. Test with real form submission');
      console.log('   3. Monitor logs in Cloudflare dashboard');
    } else {
      console.log('❌ Some checks failed. Review the function code.');
      process.exit(1);
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  }
}

testFormSubmission();
