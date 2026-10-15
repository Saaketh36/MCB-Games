#!/usr/bin/env python3
"""
MyClassboard Games Platform - Flask Backend
Complete Python backend for managing games, students, and assignments
Using PostgreSQL with SQLAlchemy ORM
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Class, Subject, Skill, Game, Teacher, Student, Assignment, Score, Analytics, ApiLog, SystemSettings, AudioFeedback
from sqlalchemy import func
import os
import sys
from datetime import datetime
import logging

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8', errors='replace')

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# PostgreSQL Database Configuration
database_url = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg2://myclassboard_user:myclassboard123@localhost:5432/myclassboard_games'
)
# Ensure proper format for psycopg2
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
    'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
    'pool_pre_ping': True,
    'echo': os.getenv('DB_ECHO', 'False').lower() == 'true'
}

# Initialize database
db.init_app(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# CURRICULUM & GAMES DATA (for in-memory references)
# ============================================================

CURRICULUM = {
    "I": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Numbers", "Addition", "Subtraction", "Shapes"],
        "Science": ["Life Skills", "Nature", "Safety"],
    },
    "II": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Numbers", "Multiplication", "Division", "Measurement"],
        "Science": ["Life Skills", "Weather", "Environment"],
    },
    "III": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Numbers", "Fractions", "Geometry", "Measurement"],
        "Science": ["Plants", "Animals", "Weather"],
    },
    "IV": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Fractions", "Decimals", "Geometry", "Data"],
        "Science": ["Ecosystems", "Body", "Weather"],
    },
    "V": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Decimals", "Percentages", "Geometry", "Algebra"],
        "Science": ["Matter", "Forces", "Life Cycles"],
    },
    "VI": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Algebra", "Geometry", "Statistics", "Ratios"],
        "Science": ["Cells", "Reproduction", "Ecology"],
    },
    "VII": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Algebra", "Geometry", "Statistics", "Probability"],
        "Science": ["Physics", "Chemistry", "Biology"],
    },
    "VIII": {
        "English": ["Listening", "Reading", "Writing", "Speaking"],
        "Mathematics": ["Algebra", "Geometry", "Statistics", "Calculus"],
        "Science": ["Physics", "Chemistry", "Biology"],
    }
}

GAMES = {
    "Listening": ["Listen & Do Adventure", "Story Time Quiz", "Audio Story Sequencing", "Sound Identification Game"],
    "Reading": ["Read & Comprehend", "Word Matching Game", "Passage Understanding", "Story Ordering Game"],
    "Writing": ["Letter Formation", "Word Construction", "Sentence Building", "Story Writing Challenge"],
    "Speaking": ["Word Pronunciation", "Rhyme Time Challenge", "Speech Practice", "Dialogue Simulation"],
    "Numbers": ["Count & Match", "Number Recognition", "Number Sequence", "Place Value Game"],
    "Addition": ["Simple Addition", "Addition Race", "Addition Stories", "Number Bonds Game"],
    "Subtraction": ["Subtraction Basics", "Subtraction Stories", "Take Away Game", "Difference Finder"],
    "Shapes": ["Shape Sorter", "Shape Matcher", "Shape Recognition", "Pattern Builder"],
    "Multiplication": ["Times Table Game", "Multiplication Race", "Array Builder", "Multiplication Stories"],
    "Division": ["Division Basics", "Division Game", "Sharing Game", "Division Stories"],
    "Measurement": ["Length Measurer", "Weight & Volume", "Time Tracker", "Measurement Converter"],
    "Fractions": ["Fraction Basics", "Fraction Matcher", "Compare Fractions", "Fraction Builder"],
    "Decimals": ["Decimal Identifier", "Decimal Operations", "Money Game", "Decimal Converter"],
    "Geometry": ["Angle Identifier", "Area Calculator", "Perimeter Game", "Shape Transformer"],
    "Data": ["Data Collector", "Chart Builder", "Graph Reader", "Data Organizer"],
    "Algebra": ["Variable Game", "Equation Solver", "Expression Builder", "Pattern Rule Finder"],
    "Statistics": ["Mean Calculator", "Median Finder", "Mode Identifier", "Data Analyzer"],
    "Probability": ["Probability Simulator", "Dice Game", "Spinner Game", "Chance Calculator"],
    "Ratios": ["Ratio Matcher", "Proportion Solver", "Scale Game", "Ratio Simplifier"],
    "Percentages": ["Percentage Calculator", "Discount Game", "Percentage Converter", "Part to Whole"],
    "Calculus": ["Rate of Change", "Derivative Visualizer", "Integral Calculator", "Limit Finder"],
    "Life Skills": ["Body Parts Game", "Senses Game", "Hygiene Challenge", "Emotions Recognizer"],
    "Nature": ["Animal Matcher", "Plant Identifier", "Habitat Game", "Food Chain Builder"],
    "Safety": ["Safety Rules Game", "Traffic Signs Quiz", "Emergency Response", "Safe Behavior Quiz"],
    "Weather": ["Weather Identifier", "Season Matcher", "Temperature Tracker", "Weather Predictor"],
    "Environment": ["Recycling Game", "Pollution Fighter", "Conservation Challenge", "Green Living Quiz"],
    "Plants": ["Plant Parts Game", "Plant Growth Simulator", "Seed Journey", "Photosynthesis Game"],
    "Animals": ["Animal Classification", "Habitat Matcher", "Animal Behavior Game", "Food Chain Game"],
    "Ecosystems": ["Food Chain Builder", "Ecosystem Simulator", "Biodiversity Game", "Habitat Creator"],
    "Body": ["Skeleton Builder", "Muscle Game", "Organ Identifier", "Digestion Journey"],
    "Matter": ["States of Matter", "Material Sorter", "Density Game", "Phase Change Simulator"],
    "Forces": ["Push & Pull Game", "Motion Simulator", "Simple Machines Game", "Force Explorer"],
    "Life Cycles": ["Butterfly Journey", "Frog Life Cycle", "Plant Growth", "Animal Stages"],
    "Cells": ["Cell Structure Game", "Cell Organelles Matcher", "Cell Division Simulator", "Microscope Adventure"],
    "Reproduction": ["Plant Reproduction", "Animal Reproduction", "Life Cycle Simulator", "Genetics Game"],
    "Ecology": ["Population Game", "Community Simulator", "Biome Matcher", "Adaptation Challenge"],
    "Physics": ["Motion Simulator", "Energy Converter", "Wave Visualizer", "Electromagnetic Game"],
    "Chemistry": ["Element Matcher", "Reaction Simulator", "Periodic Table Game", "Chemical Bonding Game"],
    "Biology": ["Photosynthesis Simulator", "Respiration Game", "Genetics Simulator", "Evolution Game"]
}

AVAILABLE_GAMES = {
    # CLASS I - ENGLISH
    'Listen & Do Adventure': 'listen_do_adventure.html',
    'Story Time Quiz': 'story_time_quiz_game.html',
    'Letter Formation': 'letter_formation.html',
    'Pronunciation Game': 'pronunciation_game.html',

    # CLASS I - MATHEMATICS
    'Count & Match': 'count_and_match.html',
    'Simple Addition': 'simple_addition.html',
    'Shape Sorter': 'shape_sorter.html',
    'Subtraction Basics': 'subtraction_basics.html',

    # CLASS I - SCIENCE
    'Life Skills Quiz': 'life_skills_quiz.html',
    'Nature Explorer': 'nature_explorer.html',
    'Safety Rules Quiz': 'safety_rules_quiz.html',

    # CLASS II - MATHEMATICS
    'Times Table Game': 'multiplication_table.html',
    'Division Basics': 'division_basics.html',
    'Measurement Quiz': 'measurement_quiz.html',

    # CLASS II - SCIENCE
    'Weather Quiz': 'weather_quiz.html',
    'Environment Game': 'environment_game.html',

    # CLASS II - ENGLISH
    'Reading Comprehension II': 'reading_comprehension_2.html',
    'Writing Practice II': 'writing_practice_2.html',
    'Speaking Practice II': 'speaking_practice_2.html',

    # CLASS III
    'Fraction Basics': 'fraction_basics.html',
    'Plant Parts Quiz': 'plant_parts_quiz.html',
    'Animal Matcher': 'animal_matcher.html',

    # CLASS IV
    'Decimal Identifier': 'decimal_identifier.html',
    'Geometry Game': 'geometry_game.html',
    'Data Collector': 'data_collector.html',
    'Ecosystem Simulator': 'ecosystem_simulator.html',
    'Body Systems Quiz': 'body_systems_quiz.html',

    # CLASS V
    'Percentage Calculator': 'percentage_calculator.html',
    'Algebra Basics': 'algebra_basics.html',
    'Matter States Quiz': 'matter_states_quiz.html',
    'Forces Game': 'forces_game.html',
    'Life Cycles Quiz': 'life_cycles_quiz.html',

    # CLASS VI
    'Ratio Game': 'ratio_game.html',
    'Statistics Quiz': 'statistics_quiz.html',
    'Cell Structure Game': 'cell_structure_game.html',
    'Cell Organelles Matcher': 'cell_organelles_matcher.html',
    'Reproduction Quiz': 'reproduction_quiz.html',
    'Ecology Game': 'ecology_game.html',

    # CLASS VII
    'Probability Game': 'probability_game.html',
    'Physics Quiz': 'physics_quiz.html',
    'Chemistry Game': 'chemistry_game.html',
    'Biology Quiz': 'biology_quiz.html',

    # CLASS VIII
    'Calculus Basics': 'calculus_basics.html',
    'Advanced Physics': 'advanced_physics.html',
    'Advanced Chemistry': 'advanced_chemistry.html',
    'Advanced Biology': 'advanced_biology.html'
}

# ============================================================
# API ROUTES - CURRICULUM & GAMES
# ============================================================

@app.route('/api/curriculum', methods=['GET'])
def get_curriculum():
    """Get all curriculum data"""
    return jsonify({
        'status': 'success',
        'curriculum': CURRICULUM,
        'total_classes': len(CURRICULUM)
    })

@app.route('/api/subjects/<class_id>', methods=['GET'])
def get_subjects(class_id):
    """Get subjects for a specific class"""
    try:
        subjects = db.session.query(Subject).filter_by(class_id=class_id).all()
        return jsonify({
            'status': 'success',
            'class': class_id,
            'subjects': [s.to_dict() for s in subjects]
        })
    except Exception as e:
        logger.error(f"Error fetching subjects: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/skills/<class_id>/<subject>', methods=['GET'])
def get_skills(class_id, subject):
    """Get skills for a specific class and subject"""
    try:
        subject_obj = db.session.query(Subject).filter_by(name=subject, class_id=class_id).first()
        if not subject_obj:
            return jsonify({'status': 'error', 'message': 'Subject not found'}), 404

        skills = db.session.query(Skill).filter_by(subject_id=subject_obj.id).all()
        return jsonify({
            'status': 'success',
            'class': class_id,
            'subject': subject,
            'skills': [s.to_dict() for s in skills]
        })
    except Exception as e:
        logger.error(f"Error fetching skills: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/games/<skill>', methods=['GET'])
def get_games(skill):
    """Get games for a specific skill"""
    try:
        skill_obj = db.session.query(Skill).filter_by(name=skill).first()
        if not skill_obj:
            return jsonify({'status': 'error', 'message': 'Skill not found'}), 404

        games = db.session.query(Game).filter_by(skill_id=skill_obj.id, is_active=True).all()
        games_with_status = [g.to_dict() for g in games]

        return jsonify({
            'status': 'success',
            'skill': skill,
            'games': games_with_status,
            'total': len(games_with_status)
        })
    except Exception as e:
        logger.error(f"Error fetching games: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/available-games', methods=['GET'])
def get_available_games():
    """Get all available games"""
    try:
        games = db.session.query(Game).filter_by(is_active=True).all()
        available_games = {g.name: g.file_path for g in games if g.file_path}
        total_defined = db.session.query(func.count(Game.id)).scalar()

        return jsonify({
            'status': 'success',
            'available_games': available_games,
            'total_available': len(available_games),
            'total_defined': total_defined
        })
    except Exception as e:
        logger.error(f"Error fetching available games: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================
# API ROUTES - ASSIGNMENTS
# ============================================================

@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    """Get all assignments"""
    try:
        assignments = db.session.query(Assignment).all()
        return jsonify({
            'status': 'success',
            'assignments': [a.to_dict() for a in assignments],
            'total': len(assignments)
        })
    except Exception as e:
        logger.error(f"Error fetching assignments: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/assignments', methods=['POST'])
def create_assignment():
    """Create a new assignment"""
    try:
        data = request.json
        required_fields = ['student_id', 'game_id', 'class_id', 'subject_id', 'skill_id']

        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        assignment = Assignment(
            student_id=data['student_id'],
            game_id=data['game_id'],
            class_id=data['class_id'],
            subject_id=data['subject_id'],
            skill_id=data['skill_id'],
            teacher_id=data.get('teacher_id'),
            assigned_by=data.get('assigned_by'),
            deadline=data.get('deadline'),
            status='pending'
        )

        db.session.add(assignment)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Assignment created',
            'assignment': assignment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating assignment: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/assignments/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    """Get specific assignment"""
    try:
        assignment = db.session.query(Assignment).filter_by(id=assignment_id).first()
        if not assignment:
            return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404

        return jsonify({'status': 'success', 'assignment': assignment.to_dict()})
    except Exception as e:
        logger.error(f"Error fetching assignment: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/assignments/<int:assignment_id>/complete', methods=['POST'])
def complete_assignment(assignment_id):
    """Mark assignment as complete with score"""
    try:
        data = request.json
        score = data.get('score')

        if score is None:
            return jsonify({'status': 'error', 'message': 'Score required'}), 400

        assignment = db.session.query(Assignment).filter_by(id=assignment_id).first()
        if not assignment:
            return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404

        assignment.status = 'completed'

        new_score = Score(
            assignment_id=assignment.id,
            student_id=assignment.student_id,
            game_id=assignment.game_id,
            class_id=assignment.class_id,
            skill_id=assignment.skill_id,
            score=score,
            max_score=data.get('max_score', 50),
            percentage=(score / data.get('max_score', 50)) * 100,
            correct_answers=data.get('correct_answers', 0),
            wrong_answers=data.get('wrong_answers', 0),
            total_questions=data.get('total_questions', 5),
            completion_time=data.get('completion_time'),
            performance_level=data.get('performance_level'),
            completed_at=datetime.utcnow()
        )

        db.session.add(new_score)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Assignment completed',
            'assignment': assignment.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing assignment: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================
# API ROUTES - STUDENTS
# ============================================================

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = db.session.query(Student).filter_by(is_active=True).all()
        return jsonify({
            'status': 'success',
            'students': [s.to_dict() for s in students],
            'total': len(students)
        })
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.json
        required_fields = ['name', 'roll_number', 'class_id']

        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        student = Student(
            name=data['name'],
            roll_number=data['roll_number'],
            class_id=data['class_id'],
            email=data.get('email'),
            phone=data.get('phone'),
            parent_name=data.get('parent_name'),
            parent_phone=data.get('parent_phone'),
            gender=data.get('gender')
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Student created',
            'student': student.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating student: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students/<int:student_id>/assignments', methods=['GET'])
def get_student_assignments(student_id):
    """Get assignments for a specific student"""
    try:
        assignments = db.session.query(Assignment).filter_by(student_id=student_id).all()
        return jsonify({
            'status': 'success',
            'student_id': student_id,
            'assignments': [a.to_dict() for a in assignments],
            'total': len(assignments)
        })
    except Exception as e:
        logger.error(f"Error fetching student assignments: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================
# API ROUTES - REPORTS & ANALYTICS
# ============================================================

@app.route('/api/reports/class/<int:class_id>', methods=['GET'])
def get_class_report(class_id):
    """Get performance report for a class"""
    try:
        assignments = db.session.query(Assignment).filter_by(class_id=class_id).all()
        scores = db.session.query(Score).filter_by(class_id=class_id).all()

        total = len(assignments)
        completed = len([a for a in assignments if a.status == 'completed'])
        pending = len([a for a in assignments if a.status == 'pending'])

        score_values = [float(s.score) for s in scores if s.score is not None]
        avg_score = sum(score_values) / len(score_values) if score_values else 0

        return jsonify({
            'status': 'success',
            'class_id': class_id,
            'total_assignments': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': f"{(completed/total*100):.1f}%" if total > 0 else "0%",
            'average_score': f"{avg_score:.1f}",
            'assignments': [a.to_dict() for a in assignments]
        })
    except Exception as e:
        logger.error(f"Error fetching class report: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/reports/skill/<int:skill_id>', methods=['GET'])
def get_skill_report(skill_id):
    """Get performance report for a skill"""
    try:
        assignments = db.session.query(Assignment).filter_by(skill_id=skill_id).all()
        scores = db.session.query(Score).filter_by(skill_id=skill_id).all()

        total = len(assignments)
        completed = len([a for a in assignments if a.status == 'completed'])

        score_values = [float(s.score) for s in scores if s.score is not None]
        avg_score = sum(score_values) / len(score_values) if score_values else 0

        return jsonify({
            'status': 'success',
            'skill_id': skill_id,
            'total_assignments': total,
            'completed': completed,
            'completion_rate': f"{(completed/total*100):.1f}%" if total > 0 else "0%",
            'average_score': f"{avg_score:.1f}",
            'assignments': [a.to_dict() for a in assignments]
        })
    except Exception as e:
        logger.error(f"Error fetching skill report: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================
# API ROUTES - AI GAME & QUIZ GENERATION
# ============================================================

from ai_helper import generate_ai_task_and_quiz

@app.route('/api/ai/generate-task', methods=['POST'])
def api_generate_ai_task():
    """AI endpoint for generating games, tasks, and quizzes automatically."""
    try:
        data = request.json or {}
        prompt = data.get('prompt', '')
        class_name = data.get('class', 'IV')
        subject = data.get('subject', 'Science')
        topic = data.get('topic', '')
        num_questions = data.get('num_questions', 3)
        difficulty = data.get('difficulty', 'Medium')
        api_key = data.get('api_key', None)

        task_data, provider = generate_ai_task_and_quiz(
            prompt=prompt,
            class_name=class_name,
            subject=subject,
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
            api_key=api_key
        )

        is_gemini = 'Gemini' in provider
        return jsonify({
            'status': 'success',
            'success': True,
            'provider': provider,
            'task': task_data,
            'data': {
                'task': task_data,
                'questions': task_data.get('questions', []),
                'source': 'gemini' if is_gemini else 'curriculum_engine'
            }
        }), 200
    except Exception as e:
        logger.error(f"Error in AI task generation: {e}")
        return jsonify({'status': 'error', 'success': False, 'message': str(e), 'error': str(e)}), 500

@app.route('/api/ai/status', methods=['GET'])
def api_ai_status():
    """Check AI integration status."""
    raw_key = os.getenv('GEMINI_API_KEY', '').strip()
    has_key = bool(raw_key and not raw_key.startswith('AQ.') and len(raw_key) > 20)
    return jsonify({
        'status': 'success',
        'success': True,
        'has_key': has_key,
        'has_gemini_key': has_key,
        'active_engine': 'gemini' if has_key else 'curriculum_engine',
        'model': 'gemini-2.5-flash / gemini-1.5-flash',
        'fallback': 'Smart Curriculum AI Engine'
    }), 200

# ============================================================
# STATIC FILES & MAIN ROUTES
# ============================================================

@app.route('/')
def index():
    """Serve main portal"""
    return send_from_directory('.', 'index.html')

# Only web assets are public. Source code, .env, SQL, dotfiles and node_modules are never served.
PUBLIC_EXTENSIONS = {'.html', '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                     '.mp3', '.wav', '.ogg', '.woff', '.woff2', '.ttf'}

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static web files"""
    parts = filename.replace('\\', '/').split('/')
    extension = os.path.splitext(filename)[1].lower()
    hidden = any(p.startswith('.') or p == 'node_modules' for p in parts)
    if not hidden and extension in PUBLIC_EXTENSIONS and os.path.isfile(filename):
        return send_from_directory('.', filename)
    return jsonify({'status': 'error', 'message': 'File not found'}), 404

# ============================================================
# REGISTER SCORING ROUTES
# ============================================================

from scoring_routes import scoring_bp
app.register_blueprint(scoring_bp)
from assignment_routes import portal_bp
app.register_blueprint(portal_bp)

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'status': 'error', 'message': 'Route not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'status': 'error', 'message': 'Server error'}), 500

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():
    """Initialize database"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

# ============================================================
# INITIALIZATION & STARTUP
# ============================================================

if __name__ == '__main__':
    try:
        init_db()
        print("=" * 60)
        print("MyClassboard Games Platform - Flask Backend")
        print("Database: PostgreSQL ✅")
        print("=" * 60)
        print(f"📚 Total Classes: {len(CURRICULUM)}")
        print(f"🎮 Total Games Defined: {sum(len(g) for g in GAMES.values())}")
        print(f"✅ Games Available: {len(AVAILABLE_GAMES)}")
        print("=" * 60)
        print("Starting Flask server on http://localhost:5000")
        print("API endpoints:")
        print("  - GET  /api/curriculum")
        print("  - GET  /api/subjects/<class_id>")
        print("  - GET  /api/skills/<class_id>/<subject>")
        print("  - GET  /api/games/<skill>")
        print("  - GET  /api/available-games")
        print("  - GET  /api/assignments")
        print("  - POST /api/assignments")
        print("  - GET  /api/assignments/<id>")
        print("  - POST /api/assignments/<id>/complete")
        print("  - GET  /api/students")
        print("  - POST /api/students")
        print("  - GET  /api/students/<id>/assignments")
        print("  - GET  /api/reports/class/<class_id>")
        print("  - GET  /api/reports/skill/<skill_id>")
        print("=" * 60)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        print(f"❌ Error: {e}")
        print("Make sure PostgreSQL is running and database credentials in .env are correct")
