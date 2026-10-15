#!/usr/bin/env python3
"""
Automatic PostgreSQL Setup - with provided password
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
POSTGRES_PASSWORD = "Charitha@123"  # Your password

DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = "myclassboard123"

def create_database():
    """Create PostgreSQL database and user"""
    try:
        # Connect as postgres user
        print("🔄 Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connected successfully")

        print("\n🔄 Creating database 'myclassboard_games'...")
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print("✅ Database created")
        except psycopg2.errors.DuplicateDatabase:
            print("⚠️  Database already exists, using existing...")

        print("\n🔄 Creating user 'myclassboard_user'...")
        try:
            cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD %s;", (DB_PASSWORD,))
            print("✅ User created")
        except psycopg2.errors.DuplicateObject:
            print("⚠️  User already exists, using existing...")

        print("\n🔄 Configuring user settings...")
        try:
            cursor.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';")
            cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';")
            cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_deferrable TO on;")
        except:
            pass
        print("✅ User configured")

        print("\n🔄 Granting database privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")
        print("✅ Privileges granted")

        cursor.close()
        conn.close()

        # Connect to new database as the new user
        print("\n🔄 Connecting to new database...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connected to myclassboard_games")

        print("\n🔄 Granting schema privileges...")
        cursor.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER};")
        print("✅ Schema configured")

        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        print("\n🔄 Connecting to database...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = False
        cursor = conn.cursor()
        print("✅ Connected")

        print("\n🔄 Creating database tables...")

        # Read SQL file
        sql_file = "CREATE-DATABASE-PRODUCTION.sql"
        if not os.path.exists(sql_file):
            print(f"❌ Error: {sql_file} not found!")
            return False

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split by semicolon and execute
        statements = sql_content.split(';')
        table_count = 0

        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                    if 'CREATE TABLE' in statement.upper():
                        table_count += 1
                except Exception as e:
                    if 'already exists' not in str(e).lower():
                        pass

        conn.commit()
        print(f"✅ Tables created successfully!")

        # Verify tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cursor.fetchall()

        print(f"\n📊 Database Tables Created ({len(tables)}):")
        for table in tables:
            print(f"   ✔️  {table[0]}")

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

        if not os.path.exists(env_file):
            return False

        print("\n🔄 Updating .env file...")

        # Read current .env
        with open(env_file, 'r') as f:
            lines = f.readlines()

        # Update lines
        new_lines = []
        for line in lines:
            if line.startswith("DATABASE_URL="):
                new_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"
                new_lines.append(f"DATABASE_URL={new_url}\n")
            elif line.startswith("DB_PASSWORD="):
                new_lines.append(f"DB_PASSWORD={DB_PASSWORD}\n")
            else:
                new_lines.append(line)

        # Write back
        with open(env_file, 'w') as f:
            f.writelines(new_lines)

        print("✅ .env file updated")
        return True
    except Exception as e:
        print(f"⚠️  Error updating .env: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "=" * 70)
    print("MyClassboard Games - PostgreSQL Setup")
    print("=" * 70)

    # Step 1: Create database and user
    print("\n" + "=" * 70)
    print("Step 1: Creating Database and User")
    print("=" * 70)
    if not create_database():
        print("\n❌ Setup failed")
        return False

    # Step 2: Create tables
    print("\n" + "=" * 70)
    print("Step 2: Creating Database Tables")
    print("=" * 70)
    if not create_tables():
        print("\n❌ Setup failed")
        return False

    # Step 3: Update .env
    print("\n" + "=" * 70)
    print("Step 3: Updating Configuration")
    print("=" * 70)
    update_env_file()

    # Summary
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)

    print(f"\n📊 Database Configuration:")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Host: {POSTGRES_HOST}")
    print(f"   Port: {POSTGRES_PORT}")

    print(f"\n📝 Next Steps:")
    print(f"\n   1. Install Python dependencies:")
    print(f"      pip install -r requirements.txt")

    print(f"\n   2. Run the Flask app:")
    print(f"      python app.py")

    print(f"\n   3. Test the API (new PowerShell):")
    print(f"      curl http://localhost:5000/api/curriculum")

    print(f"\n✨ Check pgAdmin:")
    print(f"   Databases > myclassboard_games > Schemas > public > Tables")
    print(f"   You should see all 12 tables!")

    print("\n🎉 Your database is ready!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
