-- EnergizedSEO Leads Database Schema
-- For Cloudflare D1 (managed SQLite)

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

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_submitted_at ON leads(submitted_at);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
