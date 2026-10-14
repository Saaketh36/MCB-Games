# Environment Setup Guide - MyClassboard Games

## Overview

The MyClassboard Games platform uses environment variables to manage configuration, API keys, and feature toggles. This guide explains how to set up your `.env` file properly.

---

## 🔑 Getting Your Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://aistudio.google.com/app/apikey**

### Step 2: Create or Select API Key
- Click **"Get API Key"** button
- Select **"Create API Key in new project"** or use existing project
- Google will generate a new API key

### Step 3: Copy Your Key
- Copy the API key (starts with `AIzaSy...`)
- Keep it secret and safe

### Step 4: Add to .env File
Open `.env` file in your project folder and replace:
```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Example (don't use this - get your own):
```
GEMINI_API_KEY=AIzaSyD-1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o
```

---

## 📋 Required Environment Variables

### Essential (Must Configure)

**GEMINI_API_KEY**
- What: Your Google Gemini API key
- Where: https://aistudio.google.com/app/apikey
- Why: Needed for AI-powered game content generation
- Example: `GEMINI_API_KEY=AIzaSyD-xxxxx`

### Optional (Pre-configured)

These have sensible defaults, but you can customize:

```
FLASK_ENV=development                    # dev or production
FLASK_DEBUG=True                         # Enable debug mode
FLASK_APP=app.py                         # Flask app file
WEB_PORT=8000                            # Web server port
API_PORT=5000                            # API server port
API_HOST=0.0.0.0                         # API bind address
CORS_ORIGINS=http://localhost:8000       # CORS allowed origins
LOG_LEVEL=INFO                           # Logging level
SESSION_TIMEOUT=3600                     # Session timeout (seconds)
AUDIO_ENABLED=True                       # Enable audio effects
ENABLE_AI_CONTENT_GENERATION=True        # AI content generation
ENABLE_AUDIO_SCRIPTS=True                # Audio script generation
```

---

## 🔧 .env File Location

**File Path:**
```
C:\Users\Charitha Sadineni\OneDrive\Desktop\Games\.env
```

**File Contents:**
```
# Minimum required configuration
GEMINI_API_KEY=YOUR_KEY_HERE
FLASK_ENV=development
FLASK_DEBUG=True

# Optional - use defaults if not specified
FLASK_APP=app.py
WEB_PORT=8000
API_PORT=5000
```

---

## ✅ Installation Steps

### 1. Create/Edit .env File

Create a file named `.env` in your project folder with:

```env
GEMINI_API_KEY=AIzaSyD_YOUR_ACTUAL_KEY_HERE
FLASK_ENV=development
FLASK_DEBUG=True
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.0
- Flask-CORS 4.0.0
- python-dotenv 1.0.0 (for reading .env)

### 3. Verify Installation

Check that python-dotenv is installed:
```bash
python -c "import dotenv; print('✅ python-dotenv installed')"
```

### 4. Start Servers

**Terminal 1:**
```bash
python -m http.server 8000
```

**Terminal 2:**
```bash
python app.py
```

### 5. Verify Configuration

The app will load .env automatically. Check for errors:
- Open: http://localhost:8000
- Open Browser Console: F12 → Console tab
- Look for error messages related to API key

---

## 🧪 Testing Your Setup

### Test 1: Check API Key is Loaded

Open Python console:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key[:20]}...")  # Shows first 20 characters
```

Expected output:
```
API Key loaded: AIzaSyD_xxxxxxxxxxxxx...
```

### Test 2: Try AI Content Generation

Send a test request to your API:
```bash
curl http://localhost:5000/api/generate-game \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"class":"I", "subject":"English", "skill":"Listening"}'
```

### Test 3: Check Server Logs

Both servers should print no errors related to API keys.

---

## 🔒 Security Best Practices

### ⚠️ IMPORTANT: Protect Your API Key

**DO NOT:**
- Share your API key with anyone
- Commit .env to GitHub or version control
- Post in forums or social media
- Include in bug reports or screenshots
- Email to others

**DO:**
- Keep .env in `.gitignore` (already configured)
- Rotate keys periodically
- Monitor usage in Google Cloud Console
- Use different keys for development/production

### .gitignore Check

Verify .env is ignored:
```bash
# Check if .gitignore exists
cat .gitignore | grep .env
```

Should show:
```
.env
.env.local
.env.*.local
```

---

## 📊 Gemini API Quotas & Pricing

### Free Tier (No Credit Card)
- ✅ 60 requests per minute
- ✅ Sufficient for classroom usage
- ✅ No cost
- ✅ Good for testing

### Paid Tier (Credit Card Required)
- **Input tokens**: $0.075 per 1K tokens
- **Output tokens**: $0.30 per 1K tokens
- **Rate limits**: Up to 10K requests/minute
- **Typical cost**: $1-5/month for classroom usage

### Monitor Usage
1. Go to: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/metrics
2. Check "Quota and system limits"
3. View usage statistics
4. Set up alerts for overages

---

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not found"

**Cause:** .env file not in correct location or not loaded

**Solution:**
1. Verify .env exists in project root: `C:\Users\Charitha Sadineni\OneDrive\Desktop\Games\.env`
2. Check it contains `GEMINI_API_KEY=YOUR_KEY`
3. Restart Python/Flask servers
4. Check app logs for errors

### Error: "Invalid API Key"

**Cause:** API key is wrong or expired

**Solution:**
1. Go to: https://aistudio.google.com/app/apikey
2. Verify your key is correct
3. Create a new key if old one is invalid
4. Update .env file
5. Restart servers

### Error: "Rate limit exceeded"

**Cause:** Too many API requests in short time

**Solution:**
1. Check your request rate (max 60/minute on free tier)
2. Implement request throttling
3. Upgrade to paid tier if needed
4. Check current usage at Google Cloud Console

### .env Variables Not Loading

**Cause:** Missing python-dotenv package

**Solution:**
```bash
pip install python-dotenv==1.0.0
pip install -r requirements.txt
```

### API Key Works Locally But Not on Server

**Cause:** .env not deployed to production server

**Solution:**
1. Use environment variables on server (don't commit .env)
2. Set env vars in server config/dashboard
3. For Heroku: Use config vars
4. For AWS: Use Secrets Manager
5. For Docker: Pass as build args

---

## 🚀 Configuration Examples

### Development Setup
```env
GEMINI_API_KEY=YOUR_DEV_KEY
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

### Production Setup
```env
GEMINI_API_KEY=YOUR_PROD_KEY
FLASK_ENV=production
FLASK_DEBUG=False
LOG_LEVEL=WARNING
```

### Minimal Setup (Use Defaults)
```env
GEMINI_API_KEY=AIzaSyD_YOUR_KEY_HERE
```

---

## 📝 Complete .env Template

Copy this template to create your .env file:

```env
# ============================================================
# GEMINI API CONFIGURATION
# ============================================================
GEMINI_API_KEY=

# ============================================================
# FLASK CONFIGURATION
# ============================================================
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py

# ============================================================
# SERVER CONFIGURATION
# ============================================================
WEB_PORT=8000
API_PORT=5000
API_HOST=0.0.0.0

# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DATA_DIR=./
ASSIGNMENTS_FILE=assignments.json
STUDENTS_FILE=students.json
GAMES_FILE=games-data.json

# ============================================================
# CORS CONFIGURATION
# ============================================================
CORS_ORIGINS=http://localhost:8000,http://localhost:5000

# ============================================================
# LOGGING CONFIGURATION
# ============================================================
LOG_LEVEL=INFO
LOG_FILE=app.log

# ============================================================
# FEATURES TOGGLE
# ============================================================
ENABLE_AI_CONTENT_GENERATION=True
ENABLE_AUDIO_SCRIPTS=True
ENABLE_ADAPTIVE_DIFFICULTY=True
ENABLE_POINTS_TRACKING=True
ENABLE_AUDIO_FEEDBACK=True

# ============================================================
# SESSION CONFIGURATION
# ============================================================
SESSION_TIMEOUT=3600
MAX_STUDENTS_PER_CLASS=50
MAX_GAMES_PER_SKILL=10

# ============================================================
# AUDIO CONFIGURATION
# ============================================================
AUDIO_ENABLED=True
CORRECT_SOUND_FREQUENCY=800
WRONG_SOUND_FREQUENCY=400
VOLUME_LEVEL=0.5
```

---

## ✅ Verification Checklist

After setup, verify everything:

- [ ] .env file created in project root
- [ ] GEMINI_API_KEY added to .env
- [ ] requirements.txt installed (`pip install -r requirements.txt`)
- [ ] Both servers started (Web on 8000, API on 5000)
- [ ] No error messages in console
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/audio-test.html
- [ ] Browser console (F12) shows no errors
- [ ] .env added to .gitignore (if using Git)

---

## 🆘 Quick Support Reference

| Issue | Command |
|-------|---------|
| Install deps | `pip install -r requirements.txt` |
| Check API key | `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:20])..."` |
| View current config | `cat .env` |
| Test server | `curl http://localhost:5000/api/curriculum` |
| Check Python | `python --version` |
| Reinstall deps | `pip install --upgrade -r requirements.txt` |

---

## 📚 Additional Resources

**Gemini API Documentation:**
- https://ai.google.dev/documentation
- https://ai.google.dev/tutorials/python_quickstart

**Flask Documentation:**
- https://flask.palletsprojects.com/
- https://flask-cors.readthedocs.io/

**Environment Variables Best Practices:**
- https://12factor.net/config

---

## Summary

✅ **What You Just Set Up:**
- Environment configuration system
- API key management
- Secure configuration handling
- Production-ready setup

✅ **What You Can Do Now:**
- Use AI content generation
- Run games with full features
- Deploy to production
- Scale your application

✅ **Next Steps:**
1. Add your GEMINI_API_KEY to .env
2. Reinstall requirements: `pip install -r requirements.txt`
3. Restart servers
4. Test everything works!

**Questions?** Check the troubleshooting section above or review the documentation files!

---

Last Updated: October 9, 2025  
Version: 1.0  
Status: ✅ Ready to Use
