#!/usr/bin/env python3
"""
Migration script to move data from JSON files to PostgreSQL
Run this AFTER PostgreSQL is set up and app database tables are created
"""

import json
import os
from dotenv import load_dotenv
from models import db, Class, Subject, Skill, Game, Student, Assignment, Score
from app import app
from datetime import datetime

load_dotenv()

def load_json(filepath):
    """Load JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return []

def migrate_students():
    """Migrate students from JSON to PostgreSQL"""
    print("🔄 Migrating students...")
    students_file = os.path.join(os.getcwd(), 'students.json')
    students_data = load_json(students_file)

    if not students_data:
        print("  ℹ️  No students to migrate")
        return

    try:
        with app.app_context():
            for student_data in students_data:
                existing = db.session.query(Student).filter_by(
                    roll_number=student_data.get('roll'),
                    class_id=student_data.get('class_id')
                ).first()

                if not existing:
                    student = Student(
                        name=student_data.get('name'),
                        roll_number=student_data.get('roll'),
                        class_id=student_data.get('class_id'),
                        email=student_data.get('email'),
                        is_active=True
                    )
                    db.session.add(student)

            db.session.commit()
            print(f"  ✅ Migrated {len(students_data)} students")
    except Exception as e:
        db.session.rollback()
        print(f"  ❌ Error migrating students: {e}")

def migrate_assignments():
    """Migrate assignments from JSON to PostgreSQL"""
    print("🔄 Migrating assignments...")
    assignments_file = os.path.join(os.getcwd(), 'assignments.json')
    assignments_data = load_json(assignments_file)

    if not assignments_data:
        print("  ℹ️  No assignments to migrate")
        return

    try:
        with app.app_context():
            migrated = 0
            for assign_data in assignments_data:
                # Find student by name and roll
                student = db.session.query(Student).filter_by(
                    name=assign_data.get('student'),
                    roll_number=assign_data.get('roll')
                ).first()

                if not student:
                    print(f"  ⚠️  Student not found: {assign_data.get('student')}")
                    continue

                # Find game
                game = db.session.query(Game).filter_by(
                    name=assign_data.get('game')
                ).first()

                if not game:
                    print(f"  ⚠️  Game not found: {assign_data.get('game')}")
                    continue

                existing = db.session.query(Assignment).filter_by(
                    student_id=student.id,
                    game_id=game.id
                ).first()

                if not existing:
                    assignment = Assignment(
                        student_id=student.id,
                        game_id=game.id,
                        class_id=student.class_id,
                        subject_id=game.skill.subject_id,
                        skill_id=game.skill_id,
                        status=assign_data.get('status', 'pending'),
                        assigned_date=datetime.fromisoformat(assign_data['assigned_date']) if assign_data.get('assigned_date') else datetime.utcnow()
                    )
                    db.session.add(assignment)
                    migrated += 1

            db.session.commit()
            print(f"  ✅ Migrated {migrated} assignments")
    except Exception as e:
        db.session.rollback()
        print(f"  ❌ Error migrating assignments: {e}")

def verify_database():
    """Verify database connection and schema"""
    print("🔍 Verifying database...")
    try:
        with app.app_context():
            # Test connection
            db.session.execute('SELECT 1')

            # Count records
            class_count = db.session.query(Class).count()
            subject_count = db.session.query(Subject).count()
            skill_count = db.session.query(Skill).count()
            game_count = db.session.query(Game).count()
            student_count = db.session.query(Student).count()
            assignment_count = db.session.query(Assignment).count()

            print("  ✅ Database connection: OK")
            print(f"  📊 Tables populated:")
            print(f"     - Classes: {class_count}")
            print(f"     - Subjects: {subject_count}")
            print(f"     - Skills: {skill_count}")
            print(f"     - Games: {game_count}")
            print(f"     - Students: {student_count}")
            print(f"     - Assignments: {assignment_count}")

            return True
    except Exception as e:
        print(f"  ❌ Database verification failed: {e}")
        print("     Make sure PostgreSQL is running and database schema is created")
        return False

def main():
    """Main migration function"""
    print("=" * 60)
    print("JSON to PostgreSQL Migration Tool")
    print("=" * 60)

    # Verify database first
    if not verify_database():
        print("\n❌ Migration failed. Please set up PostgreSQL first.")
        print("   See POSTGRES_SETUP.md for instructions")
        return

    print("\n🚀 Starting migration...")

    # Migrate data
    migrate_students()
    migrate_assignments()

    print("\n" + "=" * 60)
    print("✅ Migration complete!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Delete JSON files (optional backup first)")
    print("  2. Start Flask app: python app.py")
    print("  3. Access API at: http://localhost:5000/api/curriculum")

if __name__ == '__main__':
    main()
