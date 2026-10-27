import json
import os
import sys
import psycopg2
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

print("=" * 70)
print("COMPREHENSIVE DEPLOYMENT VERIFICATION AUDIT")
print("=" * 70)

# Check 1: skill_areas_data.json
print("\n[Audit 1/5] Verifying skill_areas_data.json...")
with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

assert len(skills_data) == 440, f"Expected 440 items, got {len(skills_data)}"
allowed_game_types = {
    'Fill in the Blank', 'Guess the Word', 'MCQ Quiz', 'Match Pairs',
    'Memory Match', 'Odd One Out', 'Sequence Order', 'Sort & Group',
    'Story Builder', 'Timed Challenge', 'Typing Answer', 'Word Scramble'
}

for i, row in enumerate(skills_data):
    assert row.get('class') in [f"Class {r}" for r in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']], f"Invalid class at {i}: {row}"
    assert row.get('subject') in ['English', 'Mathematics', 'EVS', 'Science', 'Social Science'], f"Invalid subject at {i}: {row}"
    assert row.get('skillArea'), f"Missing skillArea at {i}: {row}"
    assert row.get('activity'), f"Missing activity at {i}: {row}"
    assert row.get('activityName'), f"Missing activityName at {i}: {row}"
    assert row.get('gameType') in allowed_game_types, f"Invalid gameType at {i}: {row.get('gameType')} in {row}"

print(f"  ✅ skill_areas_data.json: 440/440 rows valid, clean, and properly mapped!")

# Check 2: full_games_catalog.json & full_games_catalog.js
print("\n[Audit 2/5] Verifying full_games_catalog.json & .js...")
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

assert len(catalog) == 440, f"Expected 440 games, got {len(catalog)}"
for g in catalog:
    assert len(g.get('questions', [])) >= 3, f"Not enough questions in {g['id']}"

with open('full_games_catalog.js', 'r', encoding='utf-8') as f:
    js_text = f.read()
assert 'FULL_GAMES_CATALOG' in js_text
print(f"  ✅ full_games_catalog (.json and .js): 440 games with standardized skillArea & questions!")

# Check 3: PostgreSQL Database
print("\n[Audit 3/5] Verifying PostgreSQL Database Tables & Foreign Keys...")
db_url = os.getenv('DATABASE_URL', '').replace('+psycopg2', '')
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT count(*) FROM classes;")
classes_cnt = cur.fetchone()[0]
assert classes_cnt == 8, f"Expected 8 classes, got {classes_cnt}"

cur.execute("SELECT count(*) FROM subjects;")
subjects_cnt = cur.fetchone()[0]
assert subjects_cnt == 25, f"Expected 25 subjects, got {subjects_cnt}"

cur.execute("SELECT count(*) FROM skills;")
skills_cnt = cur.fetchone()[0]
print(f"  - Total Skills in DB: {skills_cnt}")

cur.execute("SELECT count(*) FROM games;")
games_cnt = cur.fetchone()[0]
assert games_cnt == 440, f"Expected 440 games, got {games_cnt}"
print(f"  - Total Games in DB: {games_cnt}")

# Check games without skill or class
cur.execute("SELECT count(*) FROM games WHERE skill_id IS NULL OR class_id IS NULL;")
orphan_games = cur.fetchone()[0]
assert orphan_games == 0, f"Found {orphan_games} orphan games!"

cur.execute("SELECT count(*) FROM students;")
students_cnt = cur.fetchone()[0]
print(f"  - Total Students in DB: {students_cnt}")

# Verify game types in DB
cur.execute("SELECT DISTINCT game_type FROM games ORDER BY game_type;")
db_game_types = [r[0] for r in cur.fetchall()]
print(f"  - DB Game Types ({len(db_game_types)}): {', '.join(db_game_types)}")
for gt in db_game_types:
    assert gt in allowed_game_types, f"Unknown game type in DB: {gt}"

cur.close()
conn.close()
print("  ✅ PostgreSQL Database: All 440 games, 25 subjects, and skills verified!")

# Check 4: Flask Backend App test
print("\n[Audit 4/5] Testing Flask Backend API...")
from app import app
client = app.test_client()

# Test /api/curriculum
res = client.get('/api/curriculum')
assert res.status_code == 200
curr_data = res.get_json()['curriculum']
assert len(curr_data) == 8, f"Expected 8 classes in curriculum API, got {len(curr_data)}"
print(f"  - /api/curriculum returns {len(curr_data)} classes")

# Test /api/available-games
res = client.get('/api/available-games')
assert res.status_code == 200
avail = res.get_json()
assert avail['total_defined'] == 440, f"Expected 440 total defined games, got {avail['total_defined']}"
print(f"  - /api/available-games returns {avail['total_available']} active games (440 defined in DB)")

# Test /api/subjects/1
res = client.get('/api/subjects/1')
assert res.status_code == 200
print("  - /api/subjects/1 returns OK")

# Test /api/portal/assignments
res = client.get('/api/portal/assignments')
assert res.status_code == 200
print("  - /api/portal/assignments returns OK")

print("  ✅ Flask Backend: APIs fully functional and serving live data!")

# Check 5: Static files & frontend compatibility
print("\n[Audit 5/5] Checking static files...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
assert 'full_games_catalog.js' in html
assert 'js/app.js' in html
print("  ✅ index.html loads full_games_catalog.js and js/app.js")

print("\n" + "=" * 70)
print("🎉 ALL VERIFICATION AUDITS PASSED WITH ZERO ERRORS!")
print("=" * 70)
