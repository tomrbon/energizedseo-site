# Test Email Configuration ✅

**Date:** March 9, 2026  
**Status:** Ready (email logged, not sent yet)

---

## Configuration

All form submissions will send a test email to:

| Setting | Value |
|---------|-------|
| **Recipient** | `tomrbon@gmail.com` |
| **Subject** | `TEST: PLUMBING` |
| **Mode** | Test (logged, not sent) |

---

## Email Content Preview

When someone submits the form (e.g., "C. Carlin Plumbing"), you'll receive:

**To:** tomrbon@gmail.com  
**Subject:** TEST: PLUMBING

**Body:**
```
⚡ Your Free Website Mockup is Ready!

Hi [Customer Name],

Thanks for requesting a free mockup from EnergizedSEO! 
We've analyzed [Business Name] and created a custom 
website preview just for you.

📊 Quick Audit Summary
- Business: [Business Name]
- Industry: [Industry]
- Current Site: [Website URL]

🎨 Your custom mockup is ready to view:
[View Your Free Mockup →] (link to energizedseo.com/preview/[slug]/)

This mockup shows what your new, SEO-optimized website 
could look like. When you're ready to move forward, 
just reply to this email and we'll get started!

Next Steps:
1. Review your mockup
2. Reply with any changes you'd like
3. We'll build and launch your site

Questions? Just hit reply — we're here to help!

Best,
Thomas R Bonnie
EnergizedSEO.com
```

---

## Current Status

✅ **Email template created**  
✅ **Test mode enabled**  
✅ **Email logged to console**  
❌ **Email not sent yet** (needs SMTP integration)

---

## To Enable Real Email Sending

### Option 1: Zoho SMTP (Existing Setup)

Use the existing Zoho Mail configuration from the EnergizedSEO pipeline:

```javascript
// Add to lead-submission.js
const emailData = {
  to: testEmail,
  from: 'thomas@energizedseo.com',
  subject: testSubject,
  html: emailBody,
  smtp: {
    host: 'smtp.zoho.com',
    port: 587,
    secure: false,
    auth: {
      user: 'tomrbon@zoho.com',
      pass: 'WUUaVsKeVKGB' // App password
    }
  }
};

// Use a service like Resend, SendGrid, or nodemailer
```

### Option 2: Cloudflare Workers + Email Routing

1. Set up Cloudflare Email Routing for `energizedseo.com`
2. Create a Worker that sends via SMTP or API
3. Call the Worker from the Pages Function

### Option 3: Third-Party Email API

**Recommended:** [Resend](https://resend.com/) or [SendGrid](https://sendgrid.com/)

```javascript
// Example with Resend
await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${env.RESEND_API_KEY}`
  },
  body: JSON.stringify({
    from: 'EnergizedSEO <hello@energizedseo.com>',
    to: testEmail,
    subject: testSubject,
    html: emailBody
  })
});
```

---

## Testing

### 1. Deploy to Cloudflare Pages

```bash
cd ~/Code/energized-seo-tool/site
wrangler pages deploy . --project-name=energizedseo
```

### 2. Submit Test Form

Go to `https://energizedseo.pages.dev` and fill out the form:

- Name: Test User
- Email: test@example.com
- Business: C. Carlin Plumbing
- Industry: Contractor
- Message: Test submission

### 3. Check Logs

In Cloudflare Dashboard → Pages → Your Project → **Functions** → **Logs**

You should see:
```
📧 EMAIL THAT WOULD BE SENT:
To: tomrbon@gmail.com
Subject: TEST: PLUMBING
Body preview: <!DOCTYPE html>...
```

### 4. (Optional) Enable Real Sending

Once you verify the email content looks good, integrate SMTP:

1. Get API key from Resend/SendGrid
2. Add to Cloudflare Environment Variables
3. Uncomment the fetch() call in `sendTestEmail()`
4. Redeploy

---

## Production Flow

When ready for production:

```
Form Submit → Cloudflare Function → Store Lead → 
Trigger Audit → Generate Mockup → Deploy Preview → 
Send Email to CUSTOMER (not test address)
```

**Production settings:**
- `testMode = false`
- Email goes to customer's email (from form)
- Subject: "Your Free Website Mockup from EnergizedSEO"

---

## Files Modified

| File | Change |
|------|--------|
| `functions/lead-submission.js` | Added `sendTestEmail()` function |
| `js/form.js` | Updated notice to show test mode |

---

## Next Steps

1. ✅ Deploy to Cloudflare Pages
2. ✅ Test form submission
3. ✅ Verify email content in logs
4. ⏳ Integrate SMTP (Resend/SendGrid/Zoho)
5. ⏳ Test real email delivery
6. ⏳ Switch to production mode (send to customers)

---

_Built by The Boardroom | EnergizedSEO Project_
