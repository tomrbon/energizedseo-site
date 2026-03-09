# Deploy EnergizedSEO to Cloudflare Pages

## Prerequisites

1. Cloudflare account (free tier works)
2. Wrangler CLI installed: `npm install -g wrangler`
3. Authenticate: `wrangler login`

## Step 1: Create a Cloudflare Pages Project

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Workers & Pages** → **Create Application** → **Pages**
3. Click **Connect to Git**
4. Select your `energizedseo` repository
5. Configure build:
   - **Production branch:** `main`
   - **Build command:** `echo "Static site"` (or leave empty)
   - **Build output directory:** `/` (root)
6. Click **Save and Deploy**

## Step 2: Enable Functions

Cloudflare Pages Functions are automatically enabled when you have a `functions/` directory.

Our function at `/functions/lead-submission.js` will be available at `/api/lead`

## Step 3: Set Up D1 Database (Optional - for lead storage)

```bash
# Create the database
wrangler d1 create energizedseo-leads

# Note the database_id from the output
```

Update `wrangler.toml`:
```toml
[[d1_databases]]
binding = "DB"
database_name = "energizedseo-leads"
database_id = "YOUR_DATABASE_ID_HERE"
```

Create the schema:
```bash
wrangler d1 execute energizedseo-leads --file=schema.sql
```

## Step 4: Configure Environment Variables

In Cloudflare Dashboard → Pages → Your Project → **Settings** → **Environment Variables**:

| Variable | Value | Description |
|----------|-------|-------------|
| `SANDBOX_MODE` | `true` | Enable sandbox mode (no real emails) |
| `PIPELINE_WEBHOOK_URL` | (your webhook URL) | Where to send lead data |

## Step 5: Deploy

```bash
cd site

# Preview deployment
wrangler pages deploy . --project-name=energizedseo

# Or push to Git and let Cloudflare auto-deploy
git add .
git commit -m "Add Cloudflare Functions backend"
git push origin main
```

## Testing

### Test Form Submission

```bash
curl -X POST https://your-project.pages.dev/api/lead \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Test&email=test@example.com&business=Test+Plumbing&industry=contractor&website=https://example.com&message=Test+message"
```

Expected response (sandbox mode):
```json
{
  "success": true,
  "message": "Thanks! We'll analyze your site and send a custom mockup within 24 hours.",
  "sandbox_mode": true,
  "mockup_url": "https://energizedseo.com/preview/test-plumbing/"
}
```

## Database Schema

If using D1, create this table:

```sql
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT NOT NULL,
  business TEXT NOT NULL,
  industry TEXT,
  website TEXT,
  message TEXT,
  submitted_at TEXT NOT NULL,
  status TEXT DEFAULT 'new',
  audit_url TEXT,
  mockup_url TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_submitted_at ON leads(submitted_at);
```

## Production Checklist

- [ ] Set `SANDBOX_MODE=false`
- [ ] Configure D1 database
- [ ] Set up pipeline webhook URL
- [ ] Configure email sending (Zoho SMTP or Cloudflare Email Routing)
- [ ] Test full pipeline end-to-end
- [ ] Set up monitoring/alerts

## Troubleshooting

### Function not found at /api/lead
- Check that `functions/lead-submission.js` exists
- Verify deployment completed successfully
- Check Cloudflare Pages logs in dashboard

### Database errors
- Ensure D1 database is bound in wrangler.toml
- Check database_id is correct
- Verify schema is created

### CORS errors
- The `_middleware.js` adds CORS headers
- Check browser console for specific errors
