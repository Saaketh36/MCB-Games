# PostgreSQL Setup Checklist

Use this checklist to ensure everything is set up correctly.

## Prerequisites ✅

- [ ] PostgreSQL 12+ installed
  - Check: `psql --version`
- [ ] PostgreSQL server running
  - Check: `pg_isready -h localhost`
- [ ] Python 3.8+ installed
  - Check: `python --version`
- [ ] pip working
  - Check: `pip --version`

## Step 1: PostgreSQL Database Setup ✅

- [ ] Open PostgreSQL command line
  ```bash
  psql -U postgres
  ```
  
- [ ] Create database
  ```sql
  CREATE DATABASE myclassboard_games;
  ```
  - Verify: `\l` (should list new database)

- [ ] Create user
  ```sql
  CREATE USER myclassboard_user WITH PASSWORD 'your_password';
  ```
  - Verify: `\du` (should list new user)

- [ ] Set user settings
  ```sql
  ALTER ROLE myclassboard_user SET client_encoding TO 'utf8';
  ALTER ROLE myclassboard_user SET default_transaction_isolation TO 'read committed';
  ALTER ROLE myclassboard_user SET default_transaction_deferrable TO on;
  ALTER ROLE myclassboard_user SET default_time_zone TO 'UTC';
  ```

- [ ] Grant database privileges
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
  ```

- [ ] Connect to new database
  ```sql
  \c myclassboard_games
  ```

- [ ] Grant schema privileges
  ```sql
  GRANT ALL ON SCHEMA public TO myclassboard_user;
  ```

- [ ] Exit psql
  ```sql
  \q
  ```

## Step 2: Project Configuration ✅

- [ ] Update `.env` file with PostgreSQL credentials
  ```env
  DATABASE_URL=postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games
  ```
  - Verify: Open .env file and check credentials
  - **DO NOT** use default password! Change it!

- [ ] Verify .env file location
  - Should be: `c:\Users\Charitha Sadineni\OneDrive\Desktop\Games\.env`
  - Check: `cat .env | grep DATABASE_URL`

- [ ] Check other .env settings (optional)
  - FLASK_ENV=development
  - FLASK_DEBUG=True
  - All other settings are optional

## Step 3: Install Python Dependencies ✅

- [ ] Install requirements
  ```bash
  pip install -r requirements.txt
  ```
  - Verify output shows:
    - Flask==2.3.0
    - Flask-CORS==4.0.0
    - Flask-SQLAlchemy==3.0.0
    - SQLAlchemy==2.0.0
    - psycopg2-binary==2.9.9
    - python-dotenv==1.0.0

- [ ] Verify installation
  ```bash
  pip list | grep -E "Flask|SQLAlchemy|psycopg2"
  ```

## Step 4: Database Schema Creation ✅

- [ ] Check that models.py exists
  - File: `models.py`
  - Location: Same directory as app.py
  - Size: ~310 lines

- [ ] Check that app.py updated
  - Should contain: `from models import db`
  - Should contain: `SQLAlchemy database configuration`
  - Should contain: `db.create_all()` call

- [ ] Run Flask app (creates tables automatically)
  ```bash
  python app.py
  ```
  - Should see: `Database: PostgreSQL ✅`
  - Let it run for 5 seconds, then stop (Ctrl+C)

- [ ] Verify tables created in PostgreSQL
  ```bash
  psql -U myclassboard_user -d myclassboard_games
  \dt
  ```
  Should list tables:
  - [ ] classes
  - [ ] subjects
  - [ ] skills
  - [ ] games
  - [ ] teachers
  - [ ] students
  - [ ] assignments
  - [ ] scores
  - [ ] analytics
  - [ ] audio_feedback
  - [ ] api_logs
  - [ ] system_settings

## Step 5: Application Testing ✅

- [ ] Start Flask app
  ```bash
  python app.py
  ```
  - Should show: `Database: PostgreSQL ✅`
  - Should show: `Starting Flask server on http://localhost:5000`

- [ ] Test API endpoint (in another terminal)
  ```bash
  curl http://localhost:5000/api/curriculum
  ```
  - Should return JSON with curriculum data
  - Should NOT show database errors

- [ ] Test student creation
  ```bash
  curl -X POST http://localhost:5000/api/students \
    -H "Content-Type: application/json" \
    -d '{"name":"Test","roll_number":"001","class_id":1}'
  ```
  - Should return: `{"status":"success",...}`

- [ ] Stop Flask app (Ctrl+C)
  - [ ] Should stop cleanly
  - [ ] No unhandled exceptions

## Step 6: Data Migration (Optional) ✅

- [ ] Check if you have existing JSON data
  - Files to check:
    - [ ] students.json (exists?)
    - [ ] assignments.json (exists?)
    - [ ] games-data.json (exists?)

- [ ] Run migration script (if JSON files exist)
  ```bash
  python migrate_json_to_postgres.py
  ```
  - Should show: `✅ Migration complete!`
  - Should show table counts

- [ ] Verify migrated data
  ```bash
  psql -U myclassboard_user -d myclassboard_games
  SELECT COUNT(*) FROM students;
  SELECT COUNT(*) FROM assignments;
  ```

## Step 7: Documentation Review ✅

- [ ] Read QUICK_START.md
  - [ ] Understand 60-second setup
  - [ ] Know how to test API

- [ ] Read INTEGRATION_GUIDE.md
  - [ ] Understand architecture
  - [ ] Know database models

- [ ] Read POSTGRES_SETUP.md
  - [ ] Know backup procedures
  - [ ] Understand troubleshooting

- [ ] Bookmark these files for reference

## Troubleshooting Checklist ❌ → ✅

### Issue: "Connection refused"
- [ ] Is PostgreSQL running? `pg_isready`
- [ ] Is port 5432 open? (Windows firewall?)
- [ ] Did you use correct host/port in .env?

### Issue: "password authentication failed"
- [ ] Is password correct in .env?
- [ ] Did you change default password?
- [ ] Run: `ALTER USER myclassboard_user WITH PASSWORD 'new_pass';`

### Issue: "database does not exist"
- [ ] Did you create database? (psql: `\l`)
- [ ] Check database name in .env
- [ ] Create: `CREATE DATABASE myclassboard_games;`

### Issue: "permission denied"
- [ ] Did you grant privileges?
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE myclassboard_games TO myclassboard_user;
  GRANT ALL ON SCHEMA public TO myclassboard_user;
  ```

### Issue: "No module named 'models'"
- [ ] Is models.py in same directory as app.py?
- [ ] Check file exists: `ls models.py`
- [ ] Check PYTHONPATH includes current directory

### Issue: "No module named 'sqlalchemy'"
- [ ] Did you run `pip install -r requirements.txt`?
- [ ] Check: `pip list | grep SQLAlchemy`
- [ ] Reinstall: `pip install --upgrade SQLAlchemy`

### Issue: "Application does not start"
- [ ] Check .env file syntax
- [ ] Check DATABASE_URL format
- [ ] Run with debug: `python -u app.py`
- [ ] Check logs: `tail -f app.log`

## Final Verification ✅

Before considering setup complete:

- [ ] PostgreSQL database accessible
  ```bash
  psql -U myclassboard_user -d myclassboard_games -c "SELECT 1"
  ```
  Should return: `1`

- [ ] All required tables exist
  ```bash
  psql -U myclassboard_user -d myclassboard_games -c "\dt"
  ```
  Should list 12 tables

- [ ] Flask app starts without errors
  ```bash
  python app.py
  ```
  Run for 10 seconds, stop with Ctrl+C

- [ ] API responds to requests
  ```bash
  curl http://localhost:5000/api/curriculum
  ```
  Should return JSON data

- [ ] Can create records
  ```bash
  curl -X POST http://localhost:5000/api/students \
    -H "Content-Type: application/json" \
    -d '{"name":"Test","roll_number":"001","class_id":1}'
  ```
  Should return success

- [ ] Can query records
  ```bash
  curl http://localhost:5000/api/students
  ```
  Should return student data

## Summary

| Component | Status | Evidence |
|-----------|--------|----------|
| PostgreSQL | ✅ | `pg_isready` returns 0 |
| Database | ✅ | Tables visible in psql |
| Python packages | ✅ | `pip list` shows all packages |
| app.py | ✅ | Imports models, configures database |
| models.py | ✅ | File exists with 12 models |
| API working | ✅ | curl returns JSON |
| Data storage | ✅ | Can create and query records |

## Ready to Go! 🚀

If all checkboxes are ✅, you're ready to:
1. Deploy the application
2. Create students and assignments via API
3. Start tracking game performance
4. Generate reports and analytics

## Next Steps

1. Bookmark documentation for reference
2. Test with real data
3. Set up automated backups
4. Monitor application logs
5. Scale as needed

---

**Completion Date:** _______________
**Verified By:** _______________
**Notes:** ___________________________________

For help, check the **Troubleshooting Checklist** above or see:
- QUICK_START.md
- POSTGRES_SETUP.md  
- INTEGRATION_GUIDE.md
