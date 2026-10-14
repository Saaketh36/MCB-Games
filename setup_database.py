#!/usr/bin/env python3
"""
Automatic PostgreSQL Database Setup Script
Creates database, user, and all tables automatically
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection details
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = input("Enter PostgreSQL 'postgres' user password: ")

DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = input("Enter password for myclassboard_user (e.g., 'password123'): ")

def create_database():
    """Create PostgreSQL database and user"""
    try:
        # Connect as postgres user
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        print("\n🔄 Creating database...")
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print("✅ Database created: myclassboard_games")

        print("\n🔄 Creating user...")
        cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD %s;", (DB_PASSWORD,))
        print(f"✅ User created: {DB_USER}")

        print("\n🔄 Configuring user settings...")
        cursor.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_deferrable TO on;")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_time_zone TO 'UTC';")
        print("✅ User settings configured")

        print("\n🔄 Granting database privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")
        print("✅ Database privileges granted")

        cursor.close()
        conn.close()

        # Connect to new database as the new user
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = True
        cursor = conn.cursor()

        print("\n🔄 Granting schema privileges...")
        cursor.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER};")
        print("✅ Schema privileges granted")

        cursor.close()
        conn.close()

        return True
    except psycopg2.errors.DuplicateDatabase:
        print("⚠️  Database already exists. Continuing...")
        return True
    except psycopg2.errors.DuplicateObject:
        print("⚠️  User already exists. Continuing...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = False
        cursor = conn.cursor()

        print("\n🔄 Creating tables...")

        # Read SQL file
        sql_file = "CREATE-DATABASE-PRODUCTION.sql"
        if not os.path.exists(sql_file):
            print(f"❌ Error: {sql_file} not found!")
            return False

        with open(sql_file, 'r') as f:
            sql_content = f.read()

        # Split by semicolon and execute each statement
        statements = sql_content.split(';')
        table_count = 0

        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                    if 'CREATE TABLE' in statement:
                        table_count += 1
                except Exception as e:
                    # Skip if table/index/view already exists
                    if 'already exists' not in str(e):
                        print(f"⚠️  {e}")

        conn.commit()
        print(f"✅ Tables created successfully! ({table_count} tables)")

        # Verify tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()

        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   ✅ {table[0]}")

        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def update_env_file():
    """Update .env file with database credentials"""
    try:
        env_file = ".env"

        # Read current .env
        with open(env_file, 'r') as f:
            content = f.read()

        # Update DATABASE_URL
        old_url = "DATABASE_URL=postgresql://myclassboard_user:your_password@localhost:5432/myclassboard_games"
        new_url = f"DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"
        content = content.replace(old_url, new_url)

        # Also update individual settings
        content = content.replace("DB_PASSWORD=your_password", f"DB_PASSWORD={DB_PASSWORD}")

        # Write back
        with open(env_file, 'w') as f:
            f.write(content)

        print("\n✅ .env file updated with database credentials")
        return True
    except Exception as e:
        print(f"⚠️  Error updating .env: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 70)
    print("MyClassboard Games - PostgreSQL Automatic Setup")
    print("=" * 70)

    # Step 1: Create database and user
    print("\n📝 Step 1: Creating Database and User")
    print("-" * 70)
    if not create_database():
        print("\n❌ Setup failed at database creation")
        return False

    # Step 2: Create tables
    print("\n📝 Step 2: Creating Database Tables")
    print("-" * 70)
    if not create_tables():
        print("\n❌ Setup failed at table creation")
        return False

    # Step 3: Update .env
    print("\n📝 Step 3: Updating Configuration")
    print("-" * 70)
    update_env_file()

    # Summary
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print(f"\nDatabase: {DB_NAME}")
    print(f"User: {DB_USER}")
    print(f"Host: {POSTGRES_HOST}")
    print(f"Port: {POSTGRES_PORT}")
    print("\n📝 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run the app: python app.py")
    print("   3. Test API: curl http://localhost:5000/api/curriculum")
    print("\n🎉 Your PostgreSQL database is ready to use!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
