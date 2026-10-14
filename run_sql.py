#!/usr/bin/env python3
import psycopg2

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = "myclassboard123"

try:
    print("🔄 Connecting to database...")
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    conn.autocommit = False
    cursor = conn.cursor()
    print("✅ Connected\n")

    # Read and execute SQL
    print("🔄 Reading create_tables.sql...")
    with open("create_tables.sql", "r") as f:
        sql = f.read()

    print("🔄 Creating tables...")
    cursor.execute(sql)
    conn.commit()
    print("✅ Tables created!\n")

    # Verify
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
    tables = cursor.fetchall()

    print(f"📊 Tables Created: {len(tables)}\n")
    for i, table in enumerate(tables, 1):
        print(f"   {i:2d}. ✔️  {table[0]}")

    cursor.close()
    conn.close()

    if len(tables) == 12:
        print(f"\n✅ All 12 tables created successfully!")
    else:
        print(f"\n⚠️  Found {len(tables)} tables (expected 12)")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
