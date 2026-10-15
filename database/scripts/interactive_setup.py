#!/usr/bin/env python3
"""
Interactive PostgreSQL Setup Script
Asks for password and creates everything
"""

import psycopg2
from psycopg2 import sql
import os
import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432

# Database credentials
DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = "myclassboard123"

def get_postgres_password():
    """Get PostgreSQL admin password from user"""
    print("\n" + "=" * 70)
    print("PostgreSQL Authentication")
    print("=" * 70)
    print("\nEnter the PostgreSQL 'postgres' user password")
    print("(This is the password you set when installing PostgreSQL)")
    password = getpass.getpass("Password: ")
    return password

def create_database(postgres_password):
    """Create PostgreSQL database and user"""
    try:
        # Connect as postgres user
        print("\n🔄 Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user="postgres",
            password=postgres_password,
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
        cursor.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_deferrable TO on;")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_time_zone TO 'UTC';")
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
    except psycopg2.OperationalError as e:
        print(f"❌ Connection Error: {e}")
        print("\nPossible causes:")
        print("  1. PostgreSQL is not running")
        print("  2. PostgreSQL password is incorrect")
        print("  3. PostgreSQL is not installed")
        return False
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
            print(f"   Make sure you're in: C:\\Users\\Charitha Sadineni\\OneDrive\\Desktop\\Games")
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
                    if 'CREATE TABLE' in statement:
                        # Extract table name
                        table_name = statement.split('CREATE TABLE')[1].strip().split()[2]
                        print(f"   ✓ Table: {table_name}")
                        table_count += 1
                except Exception as e:
                    if 'already exists' not in str(e).lower():
                        print(f"   ⚠️  {e}")

        conn.commit()
        print(f"\n✅ Created {table_count} tables successfully!")

        # Verify tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cursor.fetchall()

        print(f"\n📊 Database Tables ({len(tables)}):")
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
            print("⚠️  .env file not found")
            return False

        print("\n🔄 Updating .env file...")

        # Read current .env
        with open(env_file, 'r') as f:
            lines = f.readlines()

        # Update lines
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith("DATABASE_URL="):
                new_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"
                new_lines.append(f"DATABASE_URL={new_url}\n")
                updated = True
            elif line.startswith("DB_PASSWORD="):
                new_lines.append(f"DB_PASSWORD={DB_PASSWORD}\n")
            else:
                new_lines.append(line)

        # Write back
        with open(env_file, 'w') as f:
            f.writelines(new_lines)

        if updated:
            print("✅ .env file updated")
        else:
            print("⚠️  DATABASE_URL not found in .env file")

        return True
    except Exception as e:
        print(f"⚠️  Error updating .env: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "=" * 70)
    print("MyClassboard Games - PostgreSQL Setup")
    print("=" * 70)

    # Get PostgreSQL password
    postgres_password = get_postgres_password()

    # Step 1: Create database and user
    print("\n" + "=" * 70)
    print("Step 1: Creating Database and User")
    print("=" * 70)
    if not create_database(postgres_password):
        print("\n❌ Setup failed at database creation")
        print("\nTroubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check that the 'postgres' password is correct")
        print("  3. Verify PostgreSQL is installed on your system")
        return False

    # Step 2: Create tables
    print("\n" + "=" * 70)
    print("Step 2: Creating Database Tables")
    print("=" * 70)
    if not create_tables():
        print("\n❌ Setup failed at table creation")
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

    print(f"\n   3. Test the API (open new PowerShell window):")
    print(f"      curl http://localhost:5000/api/curriculum")

    print(f"\n🎉 Your database is ready!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
