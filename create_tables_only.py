#!/usr/bin/env python3
"""
Create tables only - database and user already exist
"""

import psycopg2
import os

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = "myclassboard123"

def create_tables():
    """Create all database tables"""
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
        print("✅ Connected to myclassboard_games\n")

        # Read SQL file
        sql_file = "CREATE-DATABASE-PRODUCTION.sql"
        if not os.path.exists(sql_file):
            print(f"❌ Error: {sql_file} not found!")
            return False

        print("🔄 Reading CREATE-DATABASE-PRODUCTION.sql...")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        print("🔄 Creating database tables...\n")

        # Split by semicolon and execute
        statements = sql_content.split(';')
        table_count = 0

        for statement in statements:
            statement = statement.strip()

            # Skip comments and empty statements
            if not statement or statement.startswith('--') or statement.startswith('/*'):
                continue

            try:
                cursor.execute(statement)

                # Count tables created
                if 'CREATE TABLE' in statement.upper():
                    # Extract table name
                    parts = statement.split()
                    if 'IF NOT EXISTS' in statement.upper():
                        idx = [i for i, x in enumerate(parts) if x.upper() == 'EXISTS'][0]
                        table_name = parts[idx + 1].strip('(')
                    else:
                        idx = [i for i, x in enumerate(parts) if x.upper() == 'TABLE'][0]
                        table_name = parts[idx + 1].strip('(')

                    print(f"   ✅ Created table: {table_name}")
                    table_count += 1

            except Exception as e:
                error_msg = str(e)
                if 'already exists' in error_msg.lower():
                    pass  # Skip already exists errors
                else:
                    print(f"   ⚠️  {error_msg}")

        conn.commit()
        print(f"\n✅ Table creation complete!")

        # Verify tables
        print("\n🔄 Verifying tables in database...\n")
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cursor.fetchall()

        print(f"📊 Total Tables in Database: {len(tables)}\n")
        for i, table in enumerate(tables, 1):
            print(f"   {i:2d}. ✔️  {table[0]}")

        # Show if tables were created
        if len(tables) == 12:
            print("\n✅ All 12 tables created successfully!")
        elif len(tables) > 0:
            print(f"\n⚠️  Found {len(tables)} tables (expected 12)")
        else:
            print("\n⚠️  No tables found!")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Create Database Tables")
    print("=" * 70)
    print()

    if create_tables():
        print("\n" + "=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print("\nYour database is ready. Check in pgAdmin:")
        print("  Databases > myclassboard_games > Schemas > public > Tables")
        print("\nNext: python app.py")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ FAILED")
        print("=" * 70)
