#!/usr/bin/env python3
import psycopg2

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Charitha@123"
DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"

try:
    print("🔄 Connecting as postgres user...")
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=DB_NAME
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Connected\n")

    print("🔄 Fixing schema permissions...")
    cursor.execute(f"ALTER SCHEMA public OWNER TO {DB_USER};")
    cursor.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER};")
    cursor.execute(f"GRANT CREATE ON SCHEMA public TO {DB_USER};")
    print("✅ Schema permissions fixed\n")

    cursor.close()
    conn.close()

    print("✅ Now trying to create tables...\n")

    # Connect as app user
    print("🔄 Connecting as myclassboard_user...")
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=DB_USER,
        password="myclassboard123",
        database=DB_NAME
    )
    conn.autocommit = False
    cursor = conn.cursor()
    print("✅ Connected\n")

    print("🔄 Creating tables...")
    with open("create_tables.sql", "r") as f:
        sql = f.read()

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

    print("\n" + "=" * 70)
    if len(tables) == 12:
        print("✅ SUCCESS! All 12 tables created!")
    else:
        print(f"⚠️  Found {len(tables)} tables (expected 12)")
    print("=" * 70)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
