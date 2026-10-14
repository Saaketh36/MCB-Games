# MyClassboard Games - Complete System Guide

## System Overview

The portal now has **TWO SEPARATE DASHBOARDS**:

1. **Teacher Dashboard** - Generate PINs and view student reports
2. **Student Dashboard** - Enter PIN and play games

---

## 🎯 Teacher Dashboard

**URL:** `http://localhost:5000/teacher-dashboard.html`

### Tab 1: Generate PINs

#### Step 1: Select Game
- Choose: Class → Subject → Skill Area → Activity
- Example: Class I → English → Alphabet → Basic English Quiz (MCQ Quiz)

#### Step 2: Add Students & Generate PINs
1. Click **+ Add Student** to add student rows
2. Fill in for each student:
   - **Student Name** (e.g., "Aman")
   - **Roll Number** (e.g., "1")
   - **Email/Phone** (optional)

3. Click **🔑 Generate All PINs**
   - System generates unique 6-digit PIN for EACH student
   - Example output:
     | Student | Roll | PIN | Activity | Game Type | Status |
     |---------|------|-----|----------|-----------|--------|
     | Aman | 1 | 111111 | English Quiz | MCQ Quiz | ✓ Active |
     | Bhavna | 2 | 222222 | English Quiz | MCQ Quiz | ✓ Active |

### Tab 2: Student Reports
- Click **🔄 Refresh Reports**
- See all students' game scores in table format:
  - Student Name, Roll No, Activity, Game Type
  - Score, Max Score, Percentage
  - When completed

---

## 🎓 Student Dashboard

**URL:** `http://localhost:5000/student-dashboard.html`

### Student Information Display
- **Student Name** (auto-filled or entered via URL)
- **Roll Number** (auto-filled or entered via URL)
- **Class** (auto-filled or entered via URL)
- **Subject** (auto-filled or entered via URL)

### Method 1: PIN-Based Access
1. Receive PIN from teacher (e.g., "111111")
2. Enter PIN in **"Your Game PIN"** field
3. Click **🎯 Play This Game**
4. Game details appear with "▶ START PLAYING" button
5. Click to launch game

### Method 2: Automatic Assignment
1. Click **⚡ Play Available Game**
2. System assigns random approved game
3. Game details appear
4. Click "▶ START PLAYING"

---

## 📊 Data Flow

### PIN Generation (Teacher Side)
```
Teacher selects Activity 
  ↓
Adds multiple Students (Name, Roll)
  ↓
Clicks "Generate All PINs"
  ↓
System creates unique PIN for each student
  ↓
PINs stored in database with:
  - PIN (6 digits, unique)
  - Game ID, Name, Type, Class, Subject
  - Student Name, Roll Number
  - Creation timestamp
```

### Game Access (Student Side)
```
Student enters PIN or gets assigned game
  ↓
System looks up PIN → finds Game details
  ↓
Student clicks "START PLAYING"
  ↓
Redirects to: play.html?id={gameId}&studentName={name}&studentRoll={roll}
  ↓
Student plays game
  ↓
Score recorded with student info
```

### Score Recording & Reporting
```
Student completes game
  ↓
Score sent to backend via API
  ↓
Score stored with:
  - Student Name, Roll, Class
  - Game Name, Type
  - Score, Max Score, Percentage
  - Completion Time
  ↓
Teacher views in "Student Reports" tab
  ↓
Table shows all students' scores by activity
```

---

## 🔌 API Endpoints

### PIN Management
- **POST /api/portal/generate-pin**
  - Input: game_id, game_name, pin, student_name, student_roll
  - Returns: PIN created successfully

- **POST /api/portal/get-game-by-pin**
  - Input: pin
  - Returns: Game details for that PIN

- **GET /api/portal/get-random-game**
  - Returns: Random approved game

### Score Recording
- **POST /api/portal/store-student-score**
  - Input: game_id, student_name, student_roll, score, max_score, pin
  - Returns: Score saved confirmation

### Reporting
- **GET /api/portal/get-student-scores**
  - Returns: All students' scores grouped by activity

---

## 📱 Database Schema

### GamePin Table
```
- id (Primary Key)
- pin (Unique 6-digit string)
- game_id (Activity ID)
- game_name (Activity Name)
- game_type (MCQ Quiz, Match Pairs, etc.)
- game_class (Class I-VIII)
- game_subject (English, Math, etc.)
- game_skill (Skill Area)
- game_subskill (Sub-Skill Area)
- student_name (Student who will play)
- student_roll (Student roll number)
- is_approved (Boolean, default True)
- created_at (Timestamp)
- use_count (Number of times PIN was used)
```

### Score Table (Updated)
```
- id (Primary Key)
- game_id (Activity ID as string)
- student_name (Name of student)
- student_roll (Roll number)
- game_name (Activity name)
- game_type (Game type)
- pin_id (Foreign Key to GamePin)
- score (Points earned)
- max_score (Total possible points)
- percentage (Score%)
- completed_at (When game was finished)
- created_at (Timestamp)
```

---

## 🚀 Example Workflow

### Scenario: Teacher gives games to 3 students

**Teacher's Steps:**
1. Go to Teacher Dashboard → Generate PINs tab
2. Select: Class I → English → Alphabet → "Alphabet Quiz (MCQ Quiz)"
3. Add 3 students:
   - Aman, Roll 1
   - Bhavna, Roll 2
   - Chetan, Roll 3
4. Click "Generate All PINs"
5. System creates:
   - PIN 111111 → Aman
   - PIN 222222 → Bhavna
   - PIN 333333 → Chetan
6. Share PINs with students

**Student's Steps (e.g., Aman):**
1. Go to Student Dashboard
2. Sees: "Student Name: -" (can be auto-filled)
3. Enters PIN: 111111
4. Clicks "Play This Game"
5. Sees: "Alphabet Quiz (MCQ Quiz)" - Class I - English
6. Clicks "START PLAYING"
7. Plays game, gets score (e.g., 8/10)

**Teacher's Steps (After):**
1. Goes to Student Reports tab
2. Clicks "Refresh Reports"
3. Sees:
   | Student | Roll | Activity | Type | Score | % | Time |
   |---------|------|----------|------|-------|---|------|
   | Aman | 1 | Alphabet Quiz | MCQ Quiz | 8 | 80% | 2:45 |
   | Bhavna | 2 | Alphabet Quiz | MCQ Quiz | 9 | 90% | 2:10 |
   | Chetan | 3 | Alphabet Quiz | MCQ Quiz | 7 | 70% | 3:30 |

---

## 📝 Key Features

✅ **Multiple Student PIN Generation** - One activity, multiple PINs (one per student)
✅ **Student Identification** - Every score linked to name & roll
✅ **Activity Tracking** - Know which game each student played
✅ **Automatic Assignment** - Fallback if no PIN available
✅ **Score Recording** - Automatic save with student info
✅ **Teacher Reports** - Summary of all students' performance
✅ **Real-Time Updates** - Refresh to see latest scores

---

## 🔧 Running the Server

```bash
cd /path/to/Games
python app.py
```

Server runs on: `http://localhost:5000`

Access:
- **Dashboard Selector**: http://localhost:5000
- **Teacher Dashboard**: http://localhost:5000/teacher-dashboard.html
- **Student Dashboard**: http://localhost:5000/student-dashboard.html
- **Game Engine**: http://localhost:5000/play.html?id={activityId}

---

## ✅ Testing Checklist

- [ ] Teacher can select activity and add students
- [ ] System generates unique 6-digit PINs
- [ ] Student can enter PIN and see game
- [ ] Student can play game and get score
- [ ] Teacher can view all student scores in reports
- [ ] Student name and roll appear in reports
- [ ] Activity name and type appear in reports
- [ ] Multiple students can have different PINs for same activity

