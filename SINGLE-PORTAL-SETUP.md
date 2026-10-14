# Single Portal Setup - MyClassboard Games (Port 8000 Only)

## Overview

Run everything from a **single portal** at `http://localhost:8000` with no need for a separate API server.

---

## 🎯 What You'll Get

✅ **Single Portal**: http://localhost:8000  
✅ **Teacher Interface**: Assign games to students  
✅ **Student Interface**: Play assigned games  
✅ **Audio Effects**: Claps for correct, buzzer for wrong  
✅ **Points Tracking**: Real-time score display  
✅ **Data Storage**: localStorage (no database needed for now)  
✅ **All Games**: Ready to play  

---

## 🚀 How to Run (Single Command)

**That's it! Just ONE command:**

```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
python -m http.server 8000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/)
```

**Open browser:**
```
http://localhost:8000
```

---

## 📊 What's Running

| Component | Port | Status |
|-----------|------|--------|
| Web Portal (HTML/CSS/JS) | 8000 | ✅ Running |
| Teacher Interface | 8000 | ✅ Available |
| Student Interface | 8000 | ✅ Available |
| Audio System | Browser | ✅ Working |
| Points Tracker | Browser | ✅ Working |
| Data Storage | localStorage | ✅ Working |

---

## 📁 File Structure

```
C:\Users\Charitha Sadineni\OneDrive\Desktop\Games\
├── index.html (Main Portal - Teacher & Student)
├── audio-generator.js (Sound effects)
├── points-tracker.js (Points widget)
├── simple-addition.html (Game)
├── fraction-parts.html (Game)
├── listen-do-adventure-game.html (Game)
├── story-time-quiz.html (Game)
└── ... (other game files)
```

**Note:** No Flask server needed! Everything runs in the browser.

---

## 🎮 How to Use

### 1. **Open Portal**
```
http://localhost:8000
```

### 2. **Select Role**
- Click **"🏫 TEACHER"** button for teacher interface
- Click **"👨‍🎓 STUDENT"** button for student interface

### 3. **Teacher Flow**
1. Select: Class → Subject → Skill → Game
2. Enter: Student name & roll number
3. Click: "ASSIGN GAME"
4. View: Results table

### 4. **Student Flow**
1. Enter: Your name & roll number
2. Click: On your assigned game
3. Play: Answer questions
4. Hear: Audio feedback (claps/buzzer)
5. See: Points update in real-time
6. Get: Final score & feedback

---

## 📊 Games Available

| Game | Type | Points | Status |
|------|------|--------|--------|
| Simple Addition | Math | 50 | ✅ Ready |
| Fraction Parts | Math | 50 | ✅ Ready |
| Listen & Do Adventure | Listening | 50 | ✅ Ready |
| Story Time Quiz | Reading | 50 | ✅ Ready |
| Count and Match | Counting | 50 | ✅ Ready |
| Shape Sorter | Categorization | 50 | ✅ Ready |
| Multiplication Table | Math | 50 | ✅ Ready |

---

## 💾 Data Storage

Data is stored in browser's **localStorage**:

**What's Stored:**
- Student assignments
- Game scores
- Points earned
- Completion status
- Performance data

**Persists:**
- ✅ Across browser refresh (F5)
- ✅ After closing browser
- ✅ Between sessions
- ❌ Only in same browser (not other devices)

**View Data:**
- Open browser console (F12)
- Type: `JSON.parse(localStorage.getItem('mcb_assignments'))`
- Press Enter

**Clear Data (if needed):**
- Open browser console (F12)
- Type: `localStorage.clear()`
- Press Enter

---

## 🎯 Access Points

| Page | URL |
|------|-----|
| **Main Portal** | http://localhost:8000 |
| **Teacher Portal** | http://localhost:8000 (select Teacher role) |
| **Student Portal** | http://localhost:8000 (select Student role) |
| **Audio Test** | http://localhost:8000/audio-test.html |
| **Simple Addition** | http://localhost:8000/simple-addition.html |
| **Fraction Parts** | http://localhost:8000/fraction-parts.html |

---

## ✅ Verification Checklist

After starting the server:

```
[ ] Server running (see "Serving HTTP on 0.0.0.0 port 8000")
[ ] Open http://localhost:8000 in browser
[ ] Portal loads without errors
[ ] Can see "Teacher" and "Student" buttons
[ ] No red error messages in console (F12)
[ ] Click on Teacher button → works
[ ] Click on Student button → works
[ ] Can select class/subject/skill as teacher
[ ] Can play game as student
[ ] Hear audio when answering questions
[ ] See points update in real-time
```

If all checked ✅ → System fully working!

---

## 🛑 Stop Server

To stop the server:

**In the terminal:**
```
Press: Ctrl + C
```

**Confirm:**
```
Type: Y (if prompted)
Press: Enter
```

The server will stop and you'll see your terminal prompt again.

---

## ⚠️ Troubleshooting

### "Port 8000 already in use"
**Solution:**
1. Find what's using port 8000:
   ```
   netstat -ano | findstr :8000
   ```
2. Kill the process (get PID from above):
   ```
   taskkill /PID <PID> /F
   ```
3. Try again: `python -m http.server 8000`

**Or change port:**
1. Edit `.env` file
2. Change: `WEB_PORT=8000` to `WEB_PORT=8001`
3. Run: `python -m http.server 8001`
4. Access: `http://localhost:8001`

### "python not found"
**Solution:**
- Install Python from python.org
- Or check it's in PATH:
  ```
  python --version
  ```

### "Server won't start"
**Solution:**
1. Check you're in correct directory:
   ```
   cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games
   ```
2. Check directory has files:
   ```
   dir
   ```
   Should show: index.html, audio-generator.js, etc.
3. Try again: `python -m http.server 8000`

### Portal loads but looks broken
**Solution:**
1. Open console: F12
2. Look for red error messages
3. Check if all files loaded (look for 404 errors)
4. Try refreshing: Ctrl + R
5. Try hard refresh: Ctrl + Shift + R

### Audio not working
**Solution:**
1. Check system volume
2. Check browser volume
3. Allow autoplay in browser settings
4. Check console (F12) for errors
5. Try different browser

### Can't see assigned games as student
**Solution:**
1. Make sure you assigned game as teacher
2. Enter EXACT same student name (case-sensitive)
3. Enter EXACT same roll number
4. Refresh page: F5
5. Check localStorage (console: F12)

---

## 📚 Testing Guide

### Test 1: Teacher Assigns Game
1. Select role: Teacher
2. Choose: Class I → English → Listening
3. Select game: "Listen & Do Adventure"
4. Student name: John
5. Roll number: 001
6. Click: "ASSIGN GAME"
7. Verify: Game appears in Results table with status "Pending"

### Test 2: Student Plays Game
1. Refresh page (F5)
2. Select role: Student
3. Enter: John
4. Enter: 001
5. Click: On assigned game
6. Answer questions
7. Verify:
   - Audio plays (claps/buzzer)
   - Points update
   - Score shows at end
   - Status changes to "Completed"

### Test 3: Audio & Points
1. Open: http://localhost:8000/audio-test.html
2. Click: "Play Correct Sound" → hear claps ✅
3. Click: "Play Wrong Sound" → hear buzzer ✅
4. Click: "Correct Answer" → see points +10 ✅
5. Watch: Widget updates in real-time ✅

### Test 4: Data Persistence
1. Assign game as teacher
2. Play game as student
3. Complete game
4. Close browser completely
5. Reopen: http://localhost:8000
6. Check: Game still shows as "Completed"
7. Score still there ✅

---

## 🎯 Single Command Summary

**Everything you need:**

```bash
cd C:\Users\Charitha Sadineni\OneDrive\Desktop\Games && python -m http.server 8000
```

**Then open:**
```
http://localhost:8000
```

**That's it!** 🚀

---

## 📊 Feature Comparison

| Feature | Status | Details |
|---------|--------|---------|
| Teacher Portal | ✅ | Assign games, view results |
| Student Portal | ✅ | Play games, track scores |
| Audio Effects | ✅ | Claps (correct), Buzzer (wrong) |
| Points Tracking | ✅ | Real-time widget display |
| Score History | ✅ | Stored in localStorage |
| Multiple Games | ✅ | 7+ games available |
| Cascading Dropdowns | ✅ | Class → Subject → Skill |
| Data Persistence | ✅ | Survives browser refresh |
| Database (PostgreSQL) | ⏳ | Optional (for production) |
| API Server | ⏳ | Optional (for scalability) |

---

## 🚀 What's Next?

### If you want to add database later:
1. Follow: DATABASE-SETUP-GUIDE.md
2. Setup PostgreSQL
3. Migrate data from localStorage
4. Update code to use database

### If you want API server later:
1. Follow: DATABASE-SETUP-GUIDE.md
2. Run separate Flask server on port 5000
3. Update portal to fetch from API
4. More scalable for many users

### For now:
1. Run single portal (this setup)
2. Test with teachers and students
3. Verify all features work
4. Then scale up if needed

---

## ✅ Status

✅ **Single Portal**: Running  
✅ **Teacher Interface**: Ready  
✅ **Student Interface**: Ready  
✅ **Audio System**: Working  
✅ **Points Tracker**: Working  
✅ **All Games**: Available  
✅ **Data Storage**: Active  

**Ready to use!** 🎉

---

## 📞 Quick Help

**What to do:**
1. Run: `python -m http.server 8000`
2. Wait for: "Serving HTTP on..."
3. Open: `http://localhost:8000`
4. Start using!

**If something breaks:**
1. Stop server: Ctrl + C
2. Check error message
3. Read troubleshooting above
4. Restart server

**Questions?**
1. Check console (F12) for errors
2. Read this guide
3. Look at other documentation files
4. Try refreshing page (F5)

---

## 📋 Files in This Setup

Essential files (already in your folder):
```
index.html - Main portal (everything happens here)
audio-generator.js - Sound effects
points-tracker.js - Points widget
simple-addition.html - Game 1
fraction-parts.html - Game 2
listen-do-adventure-game.html - Game 3
story-time-quiz.html - Game 4
count-and-match.html - Game 5
shape-sorter.html - Game 6
multiplication-table.html - Game 7
```

All games automatically work when portal runs!

---

## 🎉 You're Ready!

Run this one command:
```bash
python -m http.server 8000
```

Then open:
```
http://localhost:8000
```

Everything else just works! 🚀

---

Last Updated: October 9, 2025  
Version: 1.0  
Status: READY TO RUN ✅
