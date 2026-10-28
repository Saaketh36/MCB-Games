#!/usr/bin/env python3
"""Assignments for the teacher/student portal, stored in PostgreSQL."""

import json
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.models import db, Score, Student, Game, Assignment, Class, Subject, Skill, GamePin

portal_bp = Blueprint('portal', __name__, url_prefix='/api/portal')

# Valid (class, subject, "Skill Area – Sub-Skill Area", activity) combinations from the curriculum PDF.
# Generated from curriculum-data.js; if the file is missing, validation is skipped.
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curriculum_catalog.json'),
              encoding='utf-8') as _f:
        CATALOG = {tuple(row) for row in json.load(_f)}
except (OSError, ValueError):
    CATALOG = None


def _get_or_create(model, defaults=None, **lookup):
    obj = db.session.query(model).filter_by(**lookup).first()
    if obj:
        return obj
    obj = model(**lookup, **(defaults or {}))
    db.session.add(obj)
    db.session.flush()
    return obj


def serialize(assignment, score=None):
    if score is None:
        score = (db.session.query(Score).filter_by(assignment_id=assignment.id)
                 .order_by(Score.id.desc()).first())
    done = assignment.status == 'completed'
    return {
        'id': assignment.id,
        'student': assignment.student.name,
        'roll': assignment.student.roll_number,
        'class': assignment.class_obj.name,
        'subject': assignment.subject.name,
        'skill': assignment.skill.name,
        'game': assignment.game.name,
        'status': assignment.status,
        'assigned_date': assignment.assigned_date.date().isoformat() if assignment.assigned_date else '',
        'deadline': assignment.deadline.date().isoformat() if assignment.deadline else '',
        'score': score.score if done and score else None,
        'max_score': score.max_score if done and score else None,
        'percentage': round(float(score.percentage or 0)) if done and score else None,
        'completed_at': score.completed_at.isoformat() if done and score and score.completed_at else None,
    }


def create_assignment(data):
    """Create a pending assignment. Returns (assignment, created)."""
    cls = _get_or_create(Class, name=str(data['class'])[:10])
    subject = _get_or_create(Subject, name=data['subject'], class_id=cls.id)
    skill = _get_or_create(Skill, name=data['skill'], subject_id=subject.id,
                           defaults={'class_id': cls.id})
    game = _get_or_create(Game, name=data['game'][:100],
                          defaults={'skill_id': skill.id, 'class_id': cls.id})
    student = _get_or_create(Student, roll_number=str(data['roll'])[:20], class_id=cls.id,
                             defaults={'name': data['student'][:100]})

    existing = db.session.query(Assignment).filter_by(
        student_id=student.id, game_id=game.id, status='pending').first()
    if existing:
        return existing, False

    deadline = None
    if data.get('deadline'):
        try:
            deadline = datetime.strptime(data['deadline'][:10], '%Y-%m-%d')
        except ValueError:
            deadline = None
    assignment = Assignment(student_id=student.id, game_id=game.id, class_id=cls.id,
                            subject_id=subject.id, skill_id=skill.id,
                            status='pending', deadline=deadline)
    db.session.add(assignment)
    db.session.flush()
    return assignment, True


REQUIRED = ['student', 'roll', 'class', 'subject', 'skill', 'game']


@portal_bp.route('/assignments', methods=['GET'])
def list_assignments():
    assignments = db.session.query(Assignment).order_by(Assignment.id).all()
    latest = {}
    for s in db.session.query(Score).order_by(Score.id).all():
        latest[s.assignment_id] = s
    return jsonify({'status': 'success',
                    'assignments': [serialize(a, latest.get(a.id)) for a in assignments]})


@portal_bp.route('/assignments/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    a = db.session.get(Assignment, assignment_id)
    if not a:
        return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404
    return jsonify({'status': 'success', 'assignment': serialize(a)})


@portal_bp.route('/assignments', methods=['POST'])
def add_assignment():
    data = request.json or {}
    missing = [f for f in REQUIRED if not str(data.get(f, '')).strip()]
    if missing:
        return jsonify({'status': 'error', 'message': 'Missing: ' + ', '.join(missing)}), 400
    if CATALOG is not None and (str(data['class']), data['subject'], data['skill'], data['game']) not in CATALOG:
        return jsonify({'status': 'error',
                        'message': 'This class, subject, skill and activity combination is not in the curriculum.'}), 400
    try:
        a, created = create_assignment(data)
        db.session.commit()
        return jsonify({'status': 'success', 'created': created,
                        'assignment': serialize(a)}), 201 if created else 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@portal_bp.route('/assignments/import', methods=['POST'])
def import_assignments():
    """One-time import of assignments that only exist in a browser's localStorage."""
    items = (request.json or {}).get('assignments', [])
    created = skipped = 0
    try:
        for item in items:
            if item.get('status') == 'completed' or any(
                    not str(item.get(f, '')).strip() for f in REQUIRED):
                skipped += 1
                continue
            _, was_new = create_assignment(item)
            created += was_new
            skipped += not was_new
        db.session.commit()
        return jsonify({'status': 'success', 'created': created, 'skipped': skipped})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# PIN-BASED GAME ACCESS
# ============================================================

@portal_bp.route('/generate-pin', methods=['POST'])
def generate_pin():
    """Generate and store a PIN for a game (teacher verification workflow)."""
    try:
        data = request.json or {}
        game_id = data.get('game_id', '').strip()
        game_name = data.get('game_name', '').strip()
        pin = data.get('pin', '').strip()

        if not all([game_id, game_name, pin]):
            return jsonify({'status': 'error', 'message': 'Missing game_id, game_name, or pin'}), 400

        # Check for duplicate PIN
        existing = db.session.query(GamePin).filter_by(pin=pin).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'PIN already exists'}), 409

        game_pin = GamePin(
            pin=pin,
            game_id=game_id,
            game_name=game_name,
            game_type=data.get('game_type'),
            game_class=data.get('game_class'),
            game_subject=data.get('game_subject'),
            game_skill=data.get('game_skill'),
            game_subskill=data.get('game_subskill'),
            is_approved=True,
            teacher_name=data.get('teacher_name', 'Teacher')
        )
        db.session.add(game_pin)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'PIN {pin} generated successfully',
            'pin': pin,
            'game_id': game_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@portal_bp.route('/get-game-by-pin', methods=['POST'])
def get_game_by_pin():
    """Student retrieves game details by entering a PIN."""
    try:
        data = request.json or {}
        pin = data.get('pin', '').strip().upper()

        if not pin:
            return jsonify({'status': 'error', 'message': 'PIN is required'}), 400

        game_pin = db.session.query(GamePin).filter_by(pin=pin, is_approved=True).first()
        if not game_pin:
            return jsonify({'status': 'error', 'message': 'Invalid or expired PIN'}), 404

        # Check if PIN was already used
        if game_pin.use_count and game_pin.use_count > 0:
            return jsonify({'status': 'error', 'message': '❌ This PIN has already been used. Please get a new PIN from your teacher.'}), 403

        return jsonify({
            'status': 'success',
            'game': {
                'id': game_pin.game_id,
                'name': game_pin.game_name,
                'type': game_pin.game_type,
                'class': game_pin.game_class or 'N/A',
                'subject': game_pin.game_subject or 'N/A',
                'skill': game_pin.game_skill or 'N/A',
                'subskill': game_pin.game_subskill or 'N/A',
                'pin': pin
            },
            'message': f'✅ Found game: {game_pin.game_name}'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@portal_bp.route('/get-random-game', methods=['GET'])
def get_random_game():
    """Student gets a random approved game when no PIN is entered."""
    try:
        from sqlalchemy import func

        # Get a random approved game
        game_pin = db.session.query(GamePin).filter_by(
            is_approved=True
        ).order_by(func.random()).first()

        if not game_pin:
            return jsonify({'status': 'error', 'message': 'No games available'}), 404

        # Increment use count
        game_pin.use_count = (game_pin.use_count or 0) + 1
        db.session.commit()

        return jsonify({
            'status': 'success',
            'game': {
                'id': game_pin.game_id,
                'name': game_pin.game_name,
                'type': game_pin.game_type,
                'class': game_pin.game_class,
                'subject': game_pin.game_subject,
                'skill': game_pin.game_skill,
                'subskill': game_pin.game_subskill,
                'pin': game_pin.pin
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@portal_bp.route('/store-student-score', methods=['POST'])
def store_student_score():
    """Store student game score with their info."""
    try:
        data = request.json or {}
        game_id = data.get('game_id', '').strip()
        student_name = data.get('student_name', 'Anonymous').strip()
        student_roll = data.get('student_roll', '').strip()
        game_name = data.get('game_name', 'Game').strip()
        game_type = data.get('game_type', '').strip()
        score = data.get('score', 0)
        max_score = data.get('max_score', 1)
        pin = data.get('pin', '').strip()

        if not all([game_id, student_name, score is not None, max_score]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # Find the PIN record
        game_pin = None
        if pin:
            game_pin = db.session.query(GamePin).filter_by(pin=pin).first()

        # Store in database (using Score model)
        from backend.models import Score
        s = Score(
            game_id=game_id,
            game_name=game_name,
            score=score,
            max_score=max_score,
            percentage=(score / max_score * 100) if max_score > 0 else 0,
            student_name=student_name,
            student_roll=student_roll,
            game_type=game_type,
            completed_at=datetime.utcnow()
        )

        if game_pin:
            s.pin_id = game_pin.id
            # Mark PIN as used (increment use_count)
            game_pin.use_count = 1
            game_pin.is_approved = False

        db.session.add(s)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Score saved for {student_name}. PIN is now locked.',
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score * 100) if max_score > 0 else 0,
            'pin_locked': True
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@portal_bp.route('/get-student-scores', methods=['GET'])
def get_student_scores():
    """Get all student scores for teacher reports."""
    try:
        from backend.models import Score
        scores = db.session.query(Score).order_by(Score.completed_at.desc()).all()

        return jsonify({
            'status': 'success',
            'scores': [
                {
                    'student_name': s.student_name,
                    'student_roll': s.student_roll,
                    'activity_name': s.game_name,
                    'game_type': s.game_type,
                    'score': s.score,
                    'max_score': s.max_score,
                    'percentage': round(float(s.percentage or 0)),
                    'completed_at': s.completed_at.isoformat() if s.completed_at else None
                }
                for s in scores
            ]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
