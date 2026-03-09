/**
 * EnergizedSEO Lead Submission Handler
 * Cloudflare Pages Function
 * 
 * Receives form submissions, stores leads, and triggers the audit pipeline
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  
  try {
    // Parse form data
    const formData = await request.formData();
    
    const lead = {
      name: formData.get('name') || '',
      email: formData.get('email') || '',
      business: formData.get('business') || '',
      industry: formData.get('industry') || '',
      website: formData.get('website') || '',
      message: formData.get('message') || '',
      submitted_at: new Date().toISOString(),
      status: 'new', // new, auditing, mockup_ready, emailed, contacted
      audit_url: null,
      mockup_url: null
    };
    
    // Validate required fields
    if (!lead.email || !lead.business) {
      return new Response(JSON.stringify({ 
        error: 'Email and business name are required' 
      }), { 
        status: 400, 
        headers: { 'Content-Type': 'application/json' } 
      });
    }
    
    // Store lead in D1 database (Cloudflare's managed SQLite)
    if (env.DB) {
      await env.DB.prepare(`
        INSERT INTO leads (name, email, business, industry, website, message, submitted_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        lead.name,
        lead.email,
        lead.business,
        lead.industry,
        lead.website,
        lead.message,
        lead.submitted_at,
        lead.status
      ).run();
    } else {
      console.warn('No D1 database configured - lead not stored');
    }
    
    // Trigger audit pipeline (async, don't wait)
    // TEST MODE: All emails go to tomrbon@gmail.com with "TEST: PLUMBING" subject
    const testMode = true; // Set to false in production
    const testEmail = 'tomrbon@gmail.com';
    const testSubject = 'TEST: PLUMBING';
    
    if (testMode) {
      console.log('TEST MODE: Sending to', testEmail);
      console.log('Lead data:', JSON.stringify(lead, null, 2));
      
      // Create a mock preview URL
      const slug = lead.business.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      lead.mockup_url = `https://energizedseo.com/preview/${slug}/`;
      lead.status = 'mockup_ready';
      
      // Update database with mockup URL
      if (env.DB && lead.mockup_url) {
        await env.DB.prepare(`
          UPDATE leads SET mockup_url = ?, status = ? WHERE email = ?
        `).bind(lead.mockup_url, lead.status, lead.email).run();
      }
      
      // Send test email to tomrbon@gmail.com
      await sendTestEmail(lead, testEmail, testSubject, env);
    } else {
      // Production: trigger full pipeline
      await triggerPipeline(lead, env);
    }
    
    // Return success response
    return new Response(JSON.stringify({
      success: true,
      message: 'Thanks! We\'ll analyze your site and send a custom mockup within 24 hours.',
      test_mode: testMode,
      test_email: testEmail,
      mockup_url: lead.mockup_url
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    console.error('Lead submission error:', error);
    
    return new Response(JSON.stringify({
      error: 'Something went wrong. Please email us at hello@energizedseo.com'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

async function sendTestEmail(lead, testEmail, testSubject, env) {
  /**
   * TEST MODE: Send email to tomrbon@gmail.com
   * Shows exactly what a customer would receive
   */
  
  const slug = lead.business.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const mockupUrl = `https://energizedseo.com/preview/${slug}/`;
  
  const emailBody = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
    .content { background: #f8f9fa; padding: 30px; }
    .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }
    .footer { background: #fff; padding: 20px; text-align: center; color: #666; font-size: 14px; border-radius: 0 0 10px 10px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>⚡ Your Free Website Mockup is Ready!</h1>
    </div>
    <div class="content">
      <p>Hi ${lead.name},</p>
      
      <p>Thanks for requesting a free mockup from <strong>EnergizedSEO</strong>! We've analyzed <strong>${lead.business}</strong> and created a custom website preview just for you.</p>
      
      <h3>📊 Quick Audit Summary</h3>
      <ul>
        <li><strong>Business:</strong> ${lead.business}</li>
        <li><strong>Industry:</strong> ${lead.industry}</li>
        <li><strong>Current Site:</strong> ${lead.website || 'Not provided'}</li>
      </ul>
      
      <p><strong>🎨 Your custom mockup is ready to view:</strong></p>
      
      <p style="text-align: center;">
        <a href="${mockupUrl}" class="button">View Your Free Mockup →</a>
      </p>
      
      <p>This mockup shows what your new, SEO-optimized website could look like. When you're ready to move forward, just reply to this email and we'll get started!</p>
      
      <p><strong>Next Steps:</strong></p>
      <ol>
        <li>Review your mockup</li>
        <li>Reply with any changes you'd like</li>
        <li>We'll build and launch your site</li>
      </ol>
      
      <p>Questions? Just hit reply — we're here to help!</p>
      
      <p>Best,<br>
      <strong>Thomas R Bonnie</strong><br>
      EnergizedSEO.com</p>
    </div>
    <div class="footer">
      <p>© 2026 EnergizedSEO. All rights reserved.</p>
      <p>This is a TEST email. No actual mockup has been generated yet.</p>
    </div>
  </div>
</body>
</html>
  `.trim();
  
  // In production, this would send via Zoho SMTP or Cloudflare Email Routing
  // For now, we'll log the email that would be sent
  console.log('\n📧 EMAIL THAT WOULD BE SENT:');
  console.log('To:', testEmail);
  console.log('Subject:', testSubject);
  console.log('Body preview:', emailBody.substring(0, 500) + '...');
  
  // TODO: When ready to send real emails, integrate with:
  // 1. Zoho Mail SMTP (existing setup from pipeline)
  // 2. Cloudflare Email Routing + Workers
  // 3. SendGrid, Postmark, or similar service
  
  // Example with fetch to a webhook that sends email:
  /*
  await fetch('https://your-server.com/api/send-email', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      to: testEmail,
      subject: testSubject,
      html: emailBody,
      lead: lead
    })
  });
  */
  
  console.log('\n✅ Test email logged (not sent - integrate SMTP to send)');
}

async function triggerPipeline(lead, env) {
  /**
   * Production pipeline trigger
   * This would:
   * 1. Run SEO audit on lead.website
   * 2. Generate mockup
   * 3. Deploy to /preview/{slug}/
   * 4. Send personalized email to customer
   */
  
  // TODO: Implement webhook call to Python pipeline
  // Example: fetch('https://your-server.com/api/audit', { method: 'POST', body: JSON.stringify(lead) })
  
  console.log('Pipeline triggered for:', lead.business);
}
