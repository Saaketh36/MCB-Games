# PostgreSQL Database Setup Guide - MyClassboard Games

## System Status

✅ **PostgreSQL Installed**: Version 18 (postgresql-x64-18)  
✅ **Service Status**: Running  
✅ **Ready for Configuration**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [User & Permissions](#user--permissions)
4. [Connection Configuration](#connection-configuration)
5. [Schema & Tables](#schema--tables)
6. [Environment Configuration](#environment-configuration)
7. [Python Integration](#python-integration)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Have
- ✅ PostgreSQL 18 installed on Windows
- ✅ PostgreSQL service running
- ✅ Flask application ready
- ✅ python-dotenv installed

### What You Need
- A PostgreSQL admin password (if set during installation)
- Python with Flask and psycopg2 library
- Access to PostgreSQL server (localhost:5432)

### Install Required Python Package

```bash
pip install psycopg2-binary==2.9.9
```

Or add to requirements.txt:
```
psycopg2-binary==2.9.9
SQLAlchemy==2.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

---

## Database Setup

### Step 1: Create Database

Open PostgreSQL command line or pgAdmin and run:

```sql
CREATE DATABASE myclassboard_games
  ENCODING 'UTF8'
  LC_COLLATE 'en_US.UTF-8'
  LC_CTYPE 'en_US.UTF-8'
  TEMPLATE template0;
```

**Alternative (using psql):**
```bash
psql -U postgres -c "CREATE DATABASE myclassboard_games ENCODING 'UTF8';"
```

### Step 2: Verify Database Created

```sql
\l  -- List all databases

-- Should show:
-- myclassboard_games | postgres | UTF8
```

Or via psql:
```bash
psql -U postgres -l | grep myclassboard_games
```

---

## User & Permissions

### Step 1: Create Database User

```sql
CREATE USER myclassboard_user WITH PASSWORD 'your_secure_password';
```

**Choose a strong password!** Example:
```sql
CREATE USER myclassboard_user WITH PASSWORD 'MyClassboard#2024!Secure';
```

### Step 2: Grant Permissions

```sql
-- Give all privileges on database
GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;

-- Give schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO myclassboard_user;

-- Grant table privileges (after tables created)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myclassboard_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myclassboard_user;
```

### Step 3: Set Default Privileges

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO myclassboard_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO myclassboard_user;
```

---

## Connection Configuration

### Connection Details

**Server:** localhost  
**Port:** 5432 (default)  
**Database:** myclassboard_games  
**User:** myclassboard_user  
**Password:** (what you set above)

### Connection String

**PostgreSQL URI Format:**
```
postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games
```

**psycopg2 Format:**
```python
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="myclassboard_games",
    user="myclassboard_user",
    password="your_password"
)
```

---

## Schema & Tables

### Step 1: Create Tables

Connect to your database:
```bash
psql -U myclassboard_user -d myclassboard_games
```

Run this SQL:

```sql
-- ============================================================
-- STUDENTS TABLE
-- ============================================================
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    class VARCHAR(10) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CLASSES TABLE
-- ============================================================
CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SUBJECTS TABLE
-- ============================================================
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, class_id)
);

-- ============================================================
-- SKILLS TABLE
-- ============================================================
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, subject_id)
);

-- ============================================================
-- GAMES TABLE
-- ============================================================
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    game_type VARCHAR(50),
    file_path VARCHAR(255),
    difficulty_level VARCHAR(20),
    max_score INT DEFAULT 50,
    questions_count INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ASSIGNMENTS TABLE
-- ============================================================
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    assigned_by VARCHAR(100),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SCORES TABLE
-- ============================================================
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    assignment_id INT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    score INT,
    max_score INT DEFAULT 50,
    correct_answers INT,
    wrong_answers INT,
    completion_time INT,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- AUDIO FEEDBACK TABLE
-- ============================================================
CREATE TABLE audio_feedback (
    id SERIAL PRIMARY KEY,
    score_id INT NOT NULL REFERENCES scores(id) ON DELETE CASCADE,
    feedback_type VARCHAR(20),
    frequency INT,
    duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ANALYTICS TABLE
-- ============================================================
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE SET NULL,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    skill_id INT REFERENCES skills(id) ON DELETE SET NULL,
    games_played INT DEFAULT 0,
    total_score INT DEFAULT 0,
    average_score DECIMAL(5,2),
    total_time_spent INT,
    last_played TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================================
CREATE INDEX idx_students_class ON students(class);
CREATE INDEX idx_assignments_student ON assignments(student_id);
CREATE INDEX idx_assignments_game ON assignments(game_id);
CREATE INDEX idx_assignments_status ON assignments(status);
CREATE INDEX idx_scores_student ON scores(student_id);
CREATE INDEX idx_scores_game ON scores(game_id);
CREATE INDEX idx_analytics_student ON analytics(student_id);
CREATE INDEX idx_analytics_class ON analytics(class_id);
```

### Step 2: Verify Tables Created

```sql
\dt  -- List all tables

-- Should show all 8 tables created above
```

---

## Environment Configuration

### Update .env File

Add these lines to your `.env` file:

```env
# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DATABASE_URL=postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myclassboard_games
DB_USER=myclassboard_user
DB_PASSWORD=your_password

# ============================================================
# DATABASE OPTIONS
# ============================================================
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_ECHO=False
DB_USE_BATCH=True
```

**IMPORTANT:** Replace `your_password` with your actual PostgreSQL password!

---

## Python Integration

### Option 1: Using psycopg2 (Direct)

Create `db_connection.py`:

```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'myclassboard_games')
        self.user = os.getenv('DB_USER', 'myclassboard_user')
        self.password = os.getenv('DB_PASSWORD', '')
    
    def connect(self):
        """Create database connection"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("✅ Connected to PostgreSQL successfully!")
            return conn
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Query executed successfully!")
            return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Update failed: {e}")
            return False

# Usage Example
if __name__ == "__main__":
    db = DatabaseConnection()
    
    # Test connection
    conn = db.connect()
    if conn:
        print("Connection test successful!")
        conn.close()
```

### Option 2: Using SQLAlchemy (ORM - Recommended)

Create `models.py`:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    class_ = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignments = db.relationship('Assignment', backref='student', lazy=True)
    scores = db.relationship('Score', backref='student', lazy=True)

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    game_type = db.Column(db.String(50))
    file_path = db.Column(db.String(255))
    max_score = db.Column(db.Integer, default=50)
    questions_count = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignments = db.relationship('Assignment', backref='game', lazy=True)
    scores = db.relationship('Score', backref='game', lazy=True)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scores = db.relationship('Score', backref='assignment', lazy=True)

class Score(db.Model):
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer, default=50)
    correct_answers = db.Column(db.Integer)
    wrong_answers = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

Update `app.py`:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://myclassboard_user:password@localhost:5432/myclassboard_games'
)
app.config['SQLALCHEMY_ECHO'] = os.getenv('DB_ECHO', 'False').lower() == 'true'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.getenv('DB_POOL_SIZE', '10')),
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}

from models import db, Student, Game, Assignment, Score
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Testing

### Test 1: Connection Test

Create `test_db_connection.py`:

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    print("✅ Successfully connected to PostgreSQL!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ PostgreSQL Version: {version[0]}")
    
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print(f"✅ Tables in database: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run:
```bash
python test_db_connection.py
```

### Test 2: Insert Data

```python
from db_connection import DatabaseConnection

db = DatabaseConnection()

# Insert student
query = """
INSERT INTO students (name, roll_number, class)
VALUES (%s, %s, %s)
"""
db.execute_update(query, ('John Doe', '001', 'I'))

# Verify
results = db.execute_query("SELECT * FROM students;")
print(results)
```

---

## Troubleshooting

### Error: "could not connect to server"

**Cause:** PostgreSQL service not running

**Solution:**
```powershell
# Start PostgreSQL service
Start-Service -Name postgresql-x64-18

# Check status
Get-Service -Name postgresql-x64-18
```

### Error: "FATAL: role does not exist"

**Cause:** User not created or wrong username

**Solution:**
```sql
-- Check existing users
\du

-- Create user if missing
CREATE USER myclassboard_user WITH PASSWORD 'your_password';
```

### Error: "database does not exist"

**Cause:** Database not created

**Solution:**
```sql
CREATE DATABASE myclassboard_games ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
```

### Error: "permission denied"

**Cause:** User doesn't have privileges

**Solution:**
```sql
GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO myclassboard_user;
```

### Connection Timeout

**Cause:** Firewall or network issue

**Solution:**
1. Check PostgreSQL service is running
2. Verify localhost:5432 is accessible
3. Check firewall settings
4. Try connecting directly: `psql -U postgres`

---

## Summary

✅ **PostgreSQL installed and running**  
✅ **Database setup guide provided**  
✅ **Python integration options shown**  
✅ **Testing procedures included**  
✅ **Troubleshooting guide available**

**Next Steps:**
1. Create database and user (see [Database Setup](#database-setup))
2. Create tables (see [Schema & Tables](#schema--tables))
3. Update .env file (see [Environment Configuration](#environment-configuration))
4. Test connection (see [Testing](#testing))
5. Integrate with Flask (see [Python Integration](#python-integration))

---

Last Updated: October 9, 2025  
Version: 1.0  
Status: Ready for Implementation
