# Deploy EnergizedSEO to Netlify

## Why Netlify?

- ✅ **Free hosting** for static sites
- ✅ **Built-in form handling** - no backend code needed
- ✅ **Automatic HTTPS** - SSL certificate included
- ✅ **Instant deploys** - push to Git and it's live
- ✅ **Form notifications** - get emailed when prospects submit

---

## Step-by-Step Deployment

### 1. Create Netlify Account

Go to **https://netlify.com** and sign up (free).

### 2. Create New Site

1. Click **"Add new site"** → **"Import an existing project"**
2. Select **GitHub**
3. Authorize Netlify to access your GitHub account
4. Find and select: **`tomrbon/energizedseo-site`**

### 3. Configure Build Settings

- **Base directory:** (leave blank)
- **Build command:** (leave blank - it's already static HTML)
- **Publish directory:** `/` (or leave blank)

### 4. Deploy!

Click **"Deploy site"**

Netlify will deploy in ~30 seconds and give you a URL like:
```
https://energizedseo-site-xxxxx.netlify.app
```

---

## Set Up Custom Domain

### 1. Go to Site Settings

In your Netlify dashboard, click on your site → **"Domain settings"**

### 2. Add Custom Domain

Click **"Add custom domain"** → Enter: `energizedseo.com`

### 3. Update DNS

Netlify will show you the nameservers to use:
```
dns1.p01.nsone.net
dns2.p01.nsone.net
dns3.p01.nsone.net
dns4.p01.nsone.net
```

**In Cloudflare:**
1. Go to your `energizedseo.com` domain
2. Remove Cloudflare nameservers
3. Update to Netlify's nameservers above

**OR** (if you want to keep Cloudflare):

Add these DNS records in Cloudflare:
```
Type: A
Name: @
Value: 75.2.60.5 (Netlify's load balancer IP)
Proxy: Disabled (gray cloud)

Type: CNAME
Name: www
Value: energizedseo-site-xxxxx.netlify.app
Proxy: Disabled
```

### 4. Enable HTTPS

Netlify automatically provisions SSL. Wait ~5 minutes and your site will be:
```
https://energizedseo.com ✅
```

---

## Set Up Form Notifications

### Option 1: Email Notifications (Default)

Netlify automatically sends form submissions to the email associated with your account.

**To change the email:**
1. Go to **Site settings** → **Forms** → **Form notifications**
2. Click **"Add notification"** → **"Email notification"**
3. Enter: `hello@energizedseo.com` (or your email)
4. Click **Save**

### Option 2: Slack Notifications

Get notified in Slack when someone submits:

1. **Site settings** → **Forms** → **Form notifications**
2. Click **"Add notification"** → **"Slack notification"**
3. Connect your Slack workspace
4. Choose the channel (e.g., `#leads`)
5. Click **Save**

### Option 3: Webhook (Advanced)

Send form data to Zapier, Make, or your own API:

1. **Site settings** → **Forms** → **Form notifications**
2. Click **"Add notification"** → **"Outgoing webhook"**
3. Enter your webhook URL
4. Click **Save**

---

## Test the Form

1. Go to your live site
2. Scroll to the contact form
3. Fill it out and submit
4. You should see the success message
5. Check your email for the submission

**Check submissions in Netlify:**
- Dashboard → Your site → **Forms** tab
- You'll see all submissions there

---

## What Happens When Someone Submits?

1. ✅ Form submits via AJAX (no page reload)
2. ✅ User sees success message
3. ✅ You get email notification
4. ✅ Submission saved in Netlify dashboard
5. ✅ You can export to CSV anytime

---

## Migration from Cloudflare Pages

### Before Switching:
- [ ] Export any analytics data from Cloudflare
- [ ] Note current DNS records in Cloudflare

### After Deploying to Netlify:
- [ ] Update nameservers (or DNS records)
- [ ] Wait for DNS propagation (5-30 min)
- [ ] Test form submission
- [ ] Set up form notifications
- [ ] Enable HTTPS

### Optional: Keep Cloudflare DNS
If you want to keep using Cloudflare's DNS (recommended for performance):
- Keep nameservers on Cloudflare
- Add Netlify's DNS records in Cloudflare dashboard
- Disable Cloudflare proxy (gray cloud, not orange)

---

## Pricing

**Netlify Free Tier:**
- ✅ Unlimited sites
- ✅ 100GB bandwidth/month
- ✅ Unlimited form submissions (100/submissions per month on free tier)
- ✅ Automatic HTTPS
- ✅ Continuous deployment from Git

**If you exceed 100 form submissions/month:**
- Upgrade to **Pro plan** ($19/month) for 1,000 submissions
- Or add **Form Functions** add-on

For most local business sites, the free tier is plenty to start.

---

## Support

- **Netlify Docs:** https://docs.netlify.com/
- **Forms Docs:** https://docs.netlify.com/forms/setup/
- **Community Forum:** https://answers.netlify.com/

---

**Ready to deploy?** Follow the steps above and you'll be live in <10 minutes! 🚀
