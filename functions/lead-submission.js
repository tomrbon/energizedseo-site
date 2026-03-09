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
    // In production, this would call a webhook or queue
    // For now, we'll log and skip the full pipeline in sandbox mode
    const sandboxMode = true; // Set to false in production
    
    if (sandboxMode) {
      console.log('SANDBOX MODE: Would trigger pipeline for:', lead.business);
      console.log('Lead data:', JSON.stringify(lead, null, 2));
      
      // For testing: create a mock preview URL
      const slug = lead.business.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      lead.mockup_url = `https://energizedseo.com/preview/${slug}/`;
      lead.status = 'mockup_ready';
      
      // Update database with mockup URL
      if (env.DB && lead.mockup_url) {
        await env.DB.prepare(`
          UPDATE leads SET mockup_url = ?, status = ? WHERE email = ?
        `).bind(lead.mockup_url, lead.status, lead.email).run();
      }
    } else {
      // Production: trigger full pipeline
      // This would call your Python pipeline via webhook or queue
      await triggerPipeline(lead, env);
    }
    
    // Return success response
    return new Response(JSON.stringify({
      success: true,
      message: 'Thanks! We\'ll analyze your site and send a custom mockup within 24 hours.',
      sandbox_mode: sandboxMode,
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

async function triggerPipeline(lead, env) {
  /**
   * Production pipeline trigger
   * This would:
   * 1. Run SEO audit on lead.website
   * 2. Generate mockup
   * 3. Deploy to /preview/{slug}/
   * 4. Send personalized email
   */
  
  // TODO: Implement webhook call to Python pipeline
  // Example: fetch('https://your-server.com/api/audit', { method: 'POST', body: JSON.stringify(lead) })
  
  console.log('Pipeline triggered for:', lead.business);
}
