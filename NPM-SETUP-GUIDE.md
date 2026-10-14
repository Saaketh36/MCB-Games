# NPM Setup Guide - MyClassboard Games

## Overview

Run MyClassboard Games using **npm** with modern development workflow.

---

## Prerequisites

### Step 1: Check if Node.js is Installed

Open Command Prompt and run:

```bash
node --version
npm --version
```

**Expected output:**
```
v18.0.0 (or higher)
9.0.0 (or higher)
```

### Step 2: If Not Installed

**Download Node.js from:** https://nodejs.org/

- Download LTS version
- Run installer
- Follow default installation steps
- Restart Command Prompt

**Verify installation:**
```bash
node --version
npm --version
```

---

## Installation & Setup

### Step 1: Navigate to Project Folder

```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
```

### Step 2: Install Dependencies

```bash
npm install
```

**What it does:**
- Creates `node_modules` folder
- Installs http-server package
- Sets up project for development

**Expected output:**
```
added X packages in Xs
```

### Step 3: Run Development Server

```bash
npm run dev
```

**Expected output:**
```
Starting up http-server, serving ./
Available on:
  http://127.0.0.1:8000
  http://localhost:8000
Hit CTRL-C to stop the server
```

### Step 4: Open Portal

Browser will auto-open, or manually open:
```
http://localhost:8000
```

---

## Available npm Commands

### Development Mode (with auto-refresh)

```bash
npm run dev
```

- Starts server on port 8000
- Auto-opens browser
- Disables caching (`-c-1`)
- Best for development

### Start Server (without auto-refresh)

```bash
npm start
```

- Starts server on port 8000
- No auto-refresh
- Disables caching
- Good for testing

### Server Only (manual cache control)

```bash
npm run server
```

- Starts server on port 8000
- Default caching behavior
- No auto-open

### API Server (Flask backend - optional)

```bash
npm run api
```

- Runs Python Flask backend on port 5000
- Requires Python installed
- Optional (not needed for basic use)

### Build (no-op for static site)

```bash
npm run build
```

- Just a placeholder command
- Static HTML files, no build needed

### Test

```bash
npm test
```

- Placeholder for test command

### Clean

```bash
npm run clean
```

- Placeholder for cleanup

---

## Quick Start Workflow

### First Time Setup

```bash
# 1. Navigate to project
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games

# 2. Install dependencies (one time only)
npm install

# 3. Start development server
npm run dev

# Browser opens automatically!
# See: http://localhost:8000
```

### Daily Use

```bash
# 1. Navigate to project
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games

# 2. Start dev server
npm run dev

# 3. Open http://localhost:8000 in browser

# 4. Use the portal!

# To stop: Press Ctrl + C in terminal
```

---

## What Gets Installed

### package.json Dependencies

**http-server** v14.1.1
- Simple HTTP server for serving static files
- Perfect for frontend-only applications
- No installation required for each use
- Fast and lightweight

### Why npm?

✅ Professional development workflow  
✅ Easy dependency management  
✅ Standard commands (`npm install`, `npm run`)  
✅ Reproducible environment  
✅ Works on Windows, Mac, Linux  
✅ Easy to scale later  

---

## Troubleshooting

### Error: "npm: command not found"

**Cause:** Node.js/npm not installed or not in PATH

**Solution:**
1. Install Node.js from https://nodejs.org
2. Restart Command Prompt
3. Try again: `npm --version`

### Error: "Port 8000 already in use"

**Solution 1: Change port in package.json**

Edit line in `package.json`:
```json
"dev": "http-server -p 8001 -c-1 -o index.html",
```

Then run:
```bash
npm run dev
```

**Solution 2: Kill existing process**

```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
npm run dev
```

### Error: "node_modules not found after npm install"

**Solution:**

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rmdir /s node_modules

# Reinstall
npm install

# Run dev server
npm run dev
```

### Server starts but browser won't open

**Solution:**

1. Check Command Prompt shows: "http://localhost:8000"
2. Manually open: http://localhost:8000 in browser
3. Refresh: Ctrl + R
4. Try different browser

### Cannot find index.html

**Solution:**

Make sure you're in correct directory:
```bash
# Check current directory
cd

# Should show: C:\Users\Charitha Sadineni\OneDrive\Desktop\Games

# Check files exist
dir

# Should show: index.html, audio-generator.js, etc.
```

---

## Project Structure

```
C:\Users\Charitha Sadineni\OneDrive\Desktop\Games\
├── package.json (npm configuration)
├── node_modules\ (created by npm install)
│   └── http-server
├── index.html (main portal)
├── audio-generator.js
├── points-tracker.js
├── simple-addition.html
├── fraction-parts.html
├── listen-do-adventure-game.html
├── story-time-quiz.html
├── count-and-match.html
├── shape-sorter.html
├── multiplication-table.html
├── .env (configuration)
└── ... (other files)
```

---

## Development Workflow

### Option 1: One Terminal (Simplest)

```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
npm run dev
```

**Result:**
- ✅ Server running on port 8000
- ✅ Browser opens automatically
- ✅ Portal accessible
- ✅ All features working

### Option 2: Two Terminals (Advanced)

**Terminal 1 - Frontend:**
```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
npm run dev
```

**Terminal 2 - Backend (optional):**
```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
npm run api
```

**Result:**
- ✅ Frontend on port 8000
- ✅ Backend API on port 5000
- ✅ Full system running

---

## npm Scripts Explained

### `npm run dev`

```bash
http-server -p 8000 -c-1 -o index.html
```

Breakdown:
- `http-server` - Start web server
- `-p 8000` - Use port 8000
- `-c-1` - Disable caching (always fresh files)
- `-o` - Open browser automatically
- `index.html` - Open this file

### `npm start`

```bash
http-server -p 8000 -c-1
```

Same as dev, but without `-o` (no auto-open)

### `npm run server`

```bash
http-server -p 8000
```

Standard http-server with default caching

---

## Stopping the Server

### In Terminal

Press: **Ctrl + C**

**You'll see:**
```
^C
Terminated batch job (Y/N)? Y
```

Type: **Y** and press **Enter**

Server stops. ✅

---

## Updating Dependencies

To update packages:

```bash
npm update
```

To see available updates:

```bash
npm outdated
```

---

## Uninstalling

If you want to remove everything:

```bash
# Remove node_modules folder
rmdir /s node_modules

# Remove package-lock.json
del package-lock.json

# Now the project is clean
```

To reinstall later:

```bash
npm install
npm run dev
```

---

## Production Deployment

For production (scalable deployment):

See: `DATABASE-SETUP-GUIDE.md` for production setup with:
- PostgreSQL database
- Flask API server
- Nginx/Apache web server
- SSL certificates

---

## Summary

| Task | Command |
|------|---------|
| First time setup | `npm install` |
| Start dev server | `npm run dev` |
| Start server | `npm start` |
| Stop server | Ctrl + C |
| Reinstall packages | `npm install` |
| Update packages | `npm update` |
| Check versions | `node --version` / `npm --version` |

---

## Success Checklist

```
[ ] Node.js installed (node --version works)
[ ] npm installed (npm --version works)
[ ] In correct directory (C:\Users\Charitha Sadineni\OneDrive\Desktop\Games)
[ ] Ran: npm install
[ ] Ran: npm run dev
[ ] Server shows: "http://localhost:8000"
[ ] Browser opened automatically
[ ] Portal visible: "MyClassboard Games Portal"
[ ] Can click Teacher button
[ ] Can click Student button
[ ] No errors in console (F12)
```

All checked? ✅ You're ready to use!

---

## Quick Reference

**One-time setup:**
```bash
npm install
```

**Every time you want to use:**
```bash
npm run dev
```

**Then open:**
```
http://localhost:8000
```

**That's it!**

---

Last Updated: October 9, 2025  
Version: 1.0  
Status: ✅ Ready to Use
