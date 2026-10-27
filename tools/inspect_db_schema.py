import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('DATABASE_URL', '').replace('+psycopg2', '')
conn = psycopg2.connect(url)
cur = conn.cursor()

for table in ['classes', 'subjects', 'skills', 'games', 'students', 'assignments']:
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position;")
    cols = cur.fetchall()
    print(f"=== Table: {table} ===")
    for c in cols:
        print(f"  {c[0]} ({c[1]})")

cur.close()
conn.close()
