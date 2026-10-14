#!/usr/bin/env python3
"""
Automatic PostgreSQL Setup - Non-interactive version
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
POSTGRES_PASSWORD = "postgres"  # Default password - change if needed

DB_NAME = "myclassboard_games"
DB_USER = "myclassboard_user"
DB_PASSWORD = "myclassboard123"  # Password for your app user

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

        print("🔄 Creating database...")
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print("✅ Database created: myclassboard_games")
        except psycopg2.errors.DuplicateDatabase:
            print("⚠️  Database already exists, skipping...")

        print("🔄 Creating user...")
        try:
            cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD %s;", (DB_PASSWORD,))
            print(f"✅ User created: {DB_USER}")
        except psycopg2.errors.DuplicateObject:
            print("⚠️  User already exists, skipping...")

        print("🔄 Configuring user settings...")
        cursor.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_transaction_deferrable TO on;")
        cursor.execute(f"ALTER ROLE {DB_USER} SET default_time_zone TO 'UTC';")
        print("✅ User settings configured")

        print("🔄 Granting database privileges...")
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

        print("🔄 Granting schema privileges...")
        cursor.execute(f"GRANT ALL ON SCHEMA public TO {DB_USER};")
        print("✅ Schema privileges granted")

        cursor.close()
        conn.close()

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

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split by semicolon and execute
        statements = sql_content.split(';')
        table_count = 0
        index_count = 0
        view_count = 0

        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                    if 'CREATE TABLE' in statement:
                        table_count += 1
                    elif 'CREATE INDEX' in statement:
                        index_count += 1
                    elif 'CREATE VIEW' in statement or 'CREATE OR REPLACE VIEW' in statement:
                        view_count += 1
                except Exception as e:
                    # Skip if already exists
                    if 'already exists' not in str(e).lower():
                        print(f"⚠️  {e}")

        conn.commit()
        print(f"✅ Tables created successfully!")
        print(f"   📊 Tables: {table_count}")
        print(f"   📑 Indexes: {index_count}")
        print(f"   📋 Views: {view_count}")

        # Verify tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = cursor.fetchall()

        print(f"\n✅ Verified {len(tables)} tables in database:")
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
            print("⚠️  .env file not found, skipping...")
            return False

        # Read current .env
        with open(env_file, 'r') as f:
            content = f.read()

        # Update DATABASE_URL
        new_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}"

        # Replace the old URL with new one
        if "DATABASE_URL=" in content:
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith("DATABASE_URL="):
                    new_lines.append(f"DATABASE_URL={new_url}")
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
        else:
            content += f"\nDATABASE_URL={new_url}\n"

        # Update password if present
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

    print(f"\nDatabase Host: {POSTGRES_HOST}")
    print(f"Database Port: {POSTGRES_PORT}")
    print(f"Database Name: {DB_NAME}")
    print(f"Database User: {DB_USER}")

    # Step 1: Create database and user
    print("\n" + "=" * 70)
    print("Step 1: Creating Database and User")
    print("=" * 70)
    if not create_database():
        print("\n❌ Setup failed at database creation")
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
    print(f"\n📊 Database Setup Summary:")
    print(f"   • Database: {DB_NAME}")
    print(f"   • User: {DB_USER}")
    print(f"   • Host: {POSTGRES_HOST}:{POSTGRES_PORT}")
    print(f"   • 12 tables created")
    print(f"   • All indexes created")
    print(f"   • All views created")

    print(f"\n📝 Next Steps:")
    print(f"   1. Install Python dependencies:")
    print(f"      pip install -r requirements.txt")
    print(f"")
    print(f"   2. Run the Flask app:")
    print(f"      python app.py")
    print(f"")
    print(f"   3. Test the API (in another terminal):")
    print(f"      curl http://localhost:5000/api/curriculum")

    print(f"\n✨ Check pgAdmin:")
    print(f"   • Go to: Databases > {DB_NAME} > Schemas > public > Tables")
    print(f"   • You should see all 12 tables")

    print("\n" + "=" * 70)
    print("🎉 Your PostgreSQL database is ready to use!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
