# PostgreSQL Integration Setup Guide

## Overview
This document guides you through setting up and connecting your Flask application to PostgreSQL.

## Prerequisites
- PostgreSQL 12+ installed and running
- Python 3.8+
- Flask environment set up

## Step 1: Create PostgreSQL Database and User

1. Open PostgreSQL command line (psql):
   ```bash
   psql -U postgres
   ```

2. Create database and user:
   ```sql
   -- Create database
   CREATE DATABASE myclassboard_games;

   -- Create user
   CREATE USER myclassboard_user WITH PASSWORD 'your_secure_password';

   -- Grant privileges
   ALTER ROLE myclassboard_user SET client_encoding TO 'utf8';
   ALTER ROLE myclassboard_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE myclassboard_user SET default_transaction_deferrable TO on;
   ALTER ROLE myclassboard_user SET default_time_zone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;

   -- Connect to database and grant schema privileges
   \c myclassboard_games
   GRANT ALL ON SCHEMA public TO myclassboard_user;
   ```

3. Exit psql:
   ```sql
   \q
   ```

## Step 2: Update Environment Variables

Edit `.env` file with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://myclassboard_user:your_secure_password@localhost:5432/myclassboard_games

# Alternative individual settings:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myclassboard_games
DB_USER=myclassboard_user
DB_PASSWORD=your_secure_password
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Initialize Database Schema

Option A: Using Flask CLI
```bash
python app.py
```
This will automatically create all tables when the app starts.

Option B: Manual SQL Script
```bash
psql -U myclassboard_user -d myclassboard_games -f CREATE-DATABASE-PRODUCTION.sql
```

## Step 5: Verify Connection

Run the Flask app:
```bash
python app.py
```

You should see:
```
========================================================
MyClassboard Games Platform - Flask Backend
Database: PostgreSQL ✅
========================================================
```

## Step 6: Test API Endpoints

Test basic connectivity:
```bash
curl http://localhost:5000/api/curriculum
```

## Troubleshooting

### Connection Error: "could not connect to server"
- Ensure PostgreSQL is running: `pg_isready -h localhost`
- Check credentials in `.env` file
- Verify database name, user, and password

### Authentication Error: "FATAL: password authentication failed"
- Verify password in `.env` matches PostgreSQL user password
- Reset password if needed:
  ```sql
  ALTER USER myclassboard_user WITH PASSWORD 'new_password';
  ```

### Import Error: "No module named 'models'"
- Ensure `models.py` is in the same directory as `app.py`
- Check all imports in app.py

### Database Already Exists
- Drop existing database:
  ```sql
  DROP DATABASE IF EXISTS myclassboard_games CASCADE;
  ```
- Create fresh database (see Step 1)

## Database Schema

The system includes these main tables:
- **classes** - Class levels (I-VIII)
- **subjects** - Subjects (English, Math, Science)
- **skills** - Learning skills within subjects
- **games** - Games linked to skills
- **students** - Student information
- **teachers** - Teacher information
- **assignments** - Game assignments to students
- **scores** - Student performance scores
- **analytics** - Aggregated analytics data
- **audio_feedback** - Audio feedback records
- **api_logs** - API request logs
- **system_settings** - Application settings

## Database Views

The system creates these views for reporting:
- **student_performance** - Individual student statistics
- **class_performance** - Class-level statistics
- **skill_performance** - Skill mastery statistics

## Backup & Restore

### Backup Database
```bash
pg_dump -U myclassboard_user -d myclassboard_games -f backup.sql
```

### Restore Database
```bash
psql -U myclassboard_user -d myclassboard_games -f backup.sql
```

## Performance Optimization

The system includes automatic indexes for:
- Student queries (class, roll number, status)
- Assignment queries (student, game, status, deadline)
- Score queries (student, game, class, skill)
- Game queries (skill, class, active status)
- Skill queries (subject, class)
- Subject queries (class)
- Analytics queries (student, class, skill)

## Next Steps

1. Populate curriculum data via API
2. Add students to classes
3. Create game assignments
4. Start tracking student performance

For more details, see API documentation in the comments within `app.py`.
