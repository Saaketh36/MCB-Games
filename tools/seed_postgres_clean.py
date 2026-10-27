import os
import sys
import psycopg2
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


load_dotenv()
db_url = os.getenv('DATABASE_URL', '').replace('+psycopg2', '')
if not db_url:
    print("No DATABASE_URL set.")
    exit(0)

conn = psycopg2.connect(db_url)
conn.autocommit = False
cur = conn.cursor()

try:
    print("Clearing old games, skills, and subjects to seed pure 440-game curriculum...")
    cur.execute("TRUNCATE TABLE assignments CASCADE;")
    cur.execute("TRUNCATE TABLE game_pins CASCADE;")
    cur.execute("TRUNCATE TABLE games CASCADE;")
    cur.execute("TRUNCATE TABLE skills CASCADE;")
    cur.execute("TRUNCATE TABLE subjects CASCADE;")
    conn.commit()

    with open('database/CREATE-DATABASE-PRODUCTION.sql', 'r', encoding='utf-8') as f:
        sql = f.read()

    cur.execute(sql)
    conn.commit()

    cur.execute("SELECT count(*) FROM classes;")
    classes_cnt = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM subjects;")
    subjects_cnt = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM skills;")
    skills_cnt = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM games;")
    games_cnt = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM students;")
    students_cnt = cur.fetchone()[0]

    print("\nDatabase Seeding Results:")
    print(f"  Classes:  {classes_cnt}")
    print(f"  Subjects: {subjects_cnt}")
    print(f"  Skills:   {skills_cnt}")
    print(f"  Games:    {games_cnt}")
    print(f"  Students: {students_cnt}")

    assert games_cnt == 440, f"Expected 440 games, got {games_cnt}"
    print("\n✅ SUCCESS: Clean 440-game database deployed successfully!")
except Exception as e:
    conn.rollback()
    print("Error during seeding:", e)
    raise
finally:
    cur.close()
    conn.close()
