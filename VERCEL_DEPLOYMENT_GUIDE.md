# 🚀 Vercel Deployment Guide

## Current Setup Status

Your Flask app is now configured for Vercel deployment:
- ✅ `vercel.json` - Serverless function configuration
- ✅ `api/index.py` - WSGI handler for Flask
- ✅ GitHub repository ready for deployment

## Prerequisites

Before running locally or deploying:

```bash
# 1. Install Node.js (required for Vercel CLI)
# Download from https://nodejs.org/

# 2. Verify installation
node --version
npm --version

# 3. Install Vercel CLI globally
npm install -g vercel
```

## Running Locally with Vercel Dev

### Step 1: Navigate to Project
```bash
cd "c:\Users\petre\OneDrive\Desktop\Meta_Insights\Python\Pandas_lesson\pd_2 assignment"
```

### Step 2: Start Vercel Dev Server
```bash
vercel dev
```

### Step 3: First-Time Setup
When you run `vercel dev` for the first time:
1. You'll be asked to log in to Vercel
2. Or create a new Vercel account
3. Follow the on-screen prompts
4. Select "Link to existing project" or "Create a new one"

### Step 4: Access Your App
```
Open http://localhost:3000 in your browser
```

## Troubleshooting

### Issue: "vercel command not found"
**Solution:** Install Vercel CLI globally
```bash
npm install -g vercel
```

### Issue: "Port 3000 already in use"
**Solution:** Use a different port
```bash
vercel dev --listen 3001
```

### Issue: Python dependencies not found
**Solution:** Ensure requirements.txt is in root directory
```bash
# Install dependencies locally for testing
pip install -r requirements.txt
```

### Issue: Database/SQLite errors
**Note:** SQLite databases won't persist on Vercel (serverless limitation)
- Local testing: Works fine with `.db` files
- Production: Consider PostgreSQL or MongoDB

## Deploying to Production

### Step 1: Connect to GitHub
```bash
vercel
```
- Select "Link to existing project"
- Choose your GitHub repo `Petrepanntech/pd-2-assignment`

### Step 2: Set Environment Variables
In Vercel Dashboard → Project Settings → Environment Variables:

```
JWT_SECRET_KEY = [generate-strong-secret]
FLASK_ENV = production
DATABASE_URL = [your-database-url-if-using-cloud-db]
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Deploy
The deployment happens automatically when you push to GitHub, or manually:
```bash
vercel --prod
```

## Project Structure for Vercel

```
├── api/
│   └── index.py          # Main WSGI handler (entry point)
├── app.py                # Flask app factory
├── config.py             # Configuration
├── models.py             # Database models
├── routes/               # API blueprints
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── [static files]       # HTML, CSS, JS
```

## Known Limitations

❌ **SQLite doesn't work for production**
- Vercel serverless functions are ephemeral
- Each request gets a fresh environment
- Database changes won't persist

✅ **Solutions:**
- Use PostgreSQL (Vercel has PostgreSQL integrations)
- Use MongoDB (cloud database)
- Use Firebase or Supabase

## Next Steps

1. **Test locally:** Run `vercel dev`
2. **Fix any errors** that appear
3. **Deploy:** Once working locally, run `vercel --prod`
4. **Monitor:** Check Vercel dashboard for logs and issues

## Resources

- [Vercel Python Guide](https://vercel.com/docs/functions/serverless-functions/python)
- [Flask on Vercel](https://vercel.com/templates/python/flask)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
