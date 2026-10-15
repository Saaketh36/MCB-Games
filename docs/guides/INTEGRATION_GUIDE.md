# PostgreSQL Integration Guide

## What Changed

Your MyClassboard Games Platform has been successfully integrated with PostgreSQL! Here's what was done:

### Files Created
1. **models.py** - SQLAlchemy ORM models for all database tables
2. **POSTGRES_SETUP.md** - Detailed PostgreSQL setup instructions
3. **migrate_json_to_postgres.py** - Migration script for existing JSON data
4. **setup_postgres.bat** - Windows setup helper script
5. **INTEGRATION_GUIDE.md** - This file

### Files Modified
1. **app.py** - Updated to use SQLAlchemy ORM instead of JSON files
2. **requirements.txt** - Added necessary dependencies

## Architecture Overview

```
┌─────────────────┐
│   Flask App     │
│   (app.py)      │
└────────┬────────┘
         │
         ├─────────────────────────┐
         │                         │
    ┌────▼────────┐        ┌───────▼──────┐
    │ SQLAlchemy  │        │   Models     │
    │  (ORM)      │        │  (models.py) │
    └────┬────────┘        └──────────────┘
         │
         └────────────────────────┐
                                  │
                          ┌───────▼──────────┐
                          │   PostgreSQL     │
                          │    Database      │
                          └──────────────────┘
```

## Key Features

### 1. Object-Relational Mapping (ORM)
- All database operations use SQLAlchemy models
- Type-safe database interactions
- Automatic relationship management

### 2. Database Models (models.py)
```python
# Example usage
from models import db, Student, Assignment, Game

# Create a student
student = Student(name="John", roll_number="001", class_id=1)
db.session.add(student)
db.session.commit()

# Query students
students = db.session.query(Student).filter_by(class_id=1).all()

# Create assignment
assignment = Assignment(
    student_id=student.id,
    game_id=1,
    class_id=1,
    subject_id=1,
    skill_id=1
)
db.session.add(assignment)
db.session.commit()
```

### 3. Automatic Table Creation
- Tables are created automatically when app.py starts
- No manual SQL execution needed (optional)
- Database schema matches PostgreSQL script

### 4. Data Migration
- Optional script to migrate existing JSON data to PostgreSQL
- Preserves all existing data
- Maintains relationships correctly

## Quick Start

### Option 1: Automated Setup (Windows)
```batch
setup_postgres.bat
```

### Option 2: Manual Setup

#### Step 1: PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE myclassboard_games;

-- Create user
CREATE USER myclassboard_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
```

#### Step 2: Update .env
```env
DATABASE_URL=postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Start App
```bash
python app.py
```

#### Step 5: Migrate Data (Optional)
```bash
python migrate_json_to_postgres.py
```

## Database Models

### Core Models

#### Student
```python
{
    'id': 1,
    'name': 'John Doe',
    'roll_number': '001',
    'class_id': 1,
    'email': 'john@school.com',
    'is_active': True
}
```

#### Assignment
```python
{
    'id': 1,
    'student_id': 1,
    'game_id': 1,
    'class_id': 1,
    'subject_id': 1,
    'skill_id': 1,
    'status': 'pending',  # pending, in_progress, completed
    'assigned_date': '2025-10-09T10:00:00',
    'deadline': '2025-10-16T10:00:00'
}
```

#### Score
```python
{
    'id': 1,
    'assignment_id': 1,
    'student_id': 1,
    'game_id': 1,
    'score': 45,
    'max_score': 50,
    'percentage': 90.0,
    'completed_at': '2025-10-09T11:30:00'
}
```

#### Analytics
```python
{
    'id': 1,
    'student_id': 1,
    'games_played': 10,
    'average_score': 85.5,
    'last_played': '2025-10-09T11:30:00'
}
```

## API Changes

### New/Updated Endpoints

#### Create Student
```http
POST /api/students
Content-Type: application/json

{
    "name": "John Doe",
    "roll_number": "001",
    "class_id": 1,
    "email": "john@school.com"
}
```

#### Get Student Assignments
```http
GET /api/students/<student_id>/assignments
```

#### Complete Assignment with Score
```http
POST /api/assignments/<assignment_id>/complete
Content-Type: application/json

{
    "score": 45,
    "max_score": 50,
    "correct_answers": 9,
    "wrong_answers": 1,
    "total_questions": 10,
    "completion_time": 300,
    "performance_level": "excellent"
}
```

## Performance Features

### Connection Pooling
```python
# Configured in app.py
pool_size = 10          # Maximum 10 connections
pool_recycle = 3600     # Recycle connections every hour
pool_pre_ping = True    # Test connections before use
```

### Automatic Indexes
- Students: class_id, roll_number, is_active
- Assignments: student_id, game_id, status, deadline
- Scores: student_id, game_id, class_id, skill_id
- Games: skill_id, class_id, is_active
- Skills: subject_id, class_id
- Analytics: student_id, class_id, skill_id

### Database Views (from SQL script)
- **student_performance** - Individual statistics
- **class_performance** - Class statistics  
- **skill_performance** - Skill mastery data

## Troubleshooting

### Connection Errors
```
Error: could not connect to server: Connection refused
```
**Solution:** Ensure PostgreSQL is running
```bash
pg_isready -h localhost
```

### Authentication Failed
```
FATAL: password authentication failed for user "myclassboard_user"
```
**Solution:** Verify credentials in .env match PostgreSQL user password

### Module Not Found
```
Error: No module named 'models'
```
**Solution:** Ensure models.py is in same directory as app.py

### Database Already Exists
```
Error: database "myclassboard_games" already exists
```
**Solution:** Drop and recreate:
```sql
DROP DATABASE myclassboard_games CASCADE;
CREATE DATABASE myclassboard_games;
```

## Monitoring & Logging

### Enable Query Logging
Edit .env:
```env
DB_ECHO=True
```

This logs all SQL queries to console.

### Log File
Check `app.log` for application logs:
```bash
tail -f app.log
```

## Backup & Restore

### Backup Database
```bash
pg_dump -U myclassboard_user -d myclassboard_games > backup.sql
```

### Restore from Backup
```bash
psql -U myclassboard_user -d myclassboard_games < backup.sql
```

## Migration Path

### From JSON to PostgreSQL
1. Update .env with PostgreSQL credentials
2. Ensure PostgreSQL database exists
3. Run app.py (creates schema)
4. Run migration script:
   ```bash
   python migrate_json_to_postgres.py
   ```
5. Verify data in PostgreSQL
6. Backup JSON files (optional delete)
7. Continue using app normally

### Rollback (if needed)
1. Keep JSON files as backup
2. Update app.py to use JSON (git revert)
3. Restore JSON from backup
4. Restart app.py

## Database Schema Diagram

```
┌──────────────┐
│   Classes    │◄────────┐
└──────────────┘         │
      │                  │
      ├─►┌──────────────┐│
      │  │   Subjects   ││
      │  └──────────────┘│
      │         │        │
      │         ├─►┌─────▼────────┐
      │         │  │    Skills    │
      │         │  └─────────────┐┘
      │         │                │
      │         │        ┌───────▼──┐
      │         │        │   Games  │
      │         │        └───────┬──┘
      │         │                │
      ├─►┌──────▼──────┐  ┌──────▼────────┐
      │  │  Students   │  │ Assignments   │
      │  └──────┬──────┘  └──────┬────────┘
      │         │                │
      │         └─────────┬──────┘
      │                   │
      │            ┌──────▼──────┐
      └───────────►│   Scores    │
                   └─────────────┘
```

## Next Steps

1. ✅ Database configured with PostgreSQL
2. ✅ ORM models created with SQLAlchemy
3. ✅ API endpoints updated for database operations
4. 📝 Add more complex queries for analytics
5. 📝 Implement caching for frequently accessed data
6. 📝 Add database transactions for complex operations
7. 📝 Set up automated backups

## Support

For detailed PostgreSQL setup, see: **POSTGRES_SETUP.md**
For API documentation, see: comments in **app.py**
For database models, see: **models.py**

## Summary

Your application now uses a professional-grade relational database (PostgreSQL) instead of JSON files. This provides:
- ✅ Better data integrity
- ✅ Improved performance with large datasets
- ✅ Advanced querying capabilities
- ✅ Built-in analytics and reporting
- ✅ Automatic relationship management
- ✅ Transaction support
- ✅ Better security for sensitive data

Happy coding! 🚀
