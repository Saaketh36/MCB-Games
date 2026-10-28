#!/usr/bin/env python3
"""
API Routes for Game Scoring and Student Performance Tracking
"""

from flask import Blueprint, request, jsonify
from backend.services.scoring_system import GameScore, StudentAnalytics, PerformanceFeedback
from backend.models import db, Score, Student, Game, Assignment, Class, Subject, Skill
from backend.routes.assignment_routes import _get_or_create

scoring_bp = Blueprint('scoring', __name__, url_prefix='/api/scoring')

# ============================================================
# GAME SUBMISSION & SCORING ENDPOINTS
# ============================================================

@scoring_bp.route('/submit', methods=['POST'])
def submit_game_score():
    """
    Submit game responses and calculate score

    Expected JSON:
    {
        "assignment_id": 1,
        "student_id": 1,
        "game_id": 1,
        "class_id": 1,
        "skill_id": 1,
        "responses": [
            {"question_id": 1, "user_answer": "A", "correct_answer": "A"},
            {"question_id": 2, "user_answer": "B", "correct_answer": "C"}
        ]
    }
    """
    try:
        data = request.json

        # Validate required fields
        required = ['assignment_id', 'student_id', 'game_id', 'class_id', 'skill_id', 'responses']
        if not all(field in data for field in required):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        # Create game score
        game_score = GameScore(
            assignment_id=data['assignment_id'],
            student_id=data['student_id'],
            game_id=data['game_id'],
            class_id=data['class_id'],
            skill_id=data['skill_id']
        )

        # Process responses
        responses_feedback = []
        for response in data['responses']:
            is_correct = response['user_answer'].lower() == response['correct_answer'].lower()
            game_score.add_response(
                question_id=response.get('question_id'),
                user_answer=response['user_answer'],
                correct_answer=response['correct_answer'],
                is_correct=is_correct
            )

            # Get feedback for each answer
            feedback = PerformanceFeedback.get_answer_feedback(
                is_correct=is_correct,
                user_answer=response['user_answer'],
                correct_answer=response['correct_answer']
            )
            responses_feedback.append({
                'question_id': response.get('question_id'),
                'feedback': feedback
            })

        # Save to database
        result = game_score.save_to_database()

        if result['success']:
            score_obj = db.session.query(Score).get(result['score_id'])
            visual_feedback = PerformanceFeedback.get_visual_feedback(score_obj)

            return jsonify({
                'status': 'success',
                'message': 'Score submitted successfully',
                'score_id': result['score_id'],
                'score_data': result['score_data'],
                'visual_feedback': visual_feedback,
                'responses_feedback': responses_feedback
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': result['message']
            }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@scoring_bp.route('/completed', methods=['GET'])
def completed_games():
    """Latest recorded score per (student roll, class, game) for syncing the UI."""
    rows = (db.session.query(Score, Student, Game, Class)
            .join(Student, Score.student_id == Student.id)
            .join(Game, Score.game_id == Game.id)
            .join(Class, Score.class_id == Class.id)
            .order_by(Score.id).all())
    latest = {}
    for score, student, game, cls in rows:
        latest[(student.roll_number, cls.name, game.name)] = {
            'roll': student.roll_number, 'student': student.name, 'class': cls.name,
            'game': game.name, 'score': score.score, 'max_score': score.max_score,
            'percentage': float(score.percentage or 0),
            'completed_at': score.completed_at.isoformat() if score.completed_at else None}
    return jsonify({'status': 'success', 'completed': list(latest.values())})


@scoring_bp.route('/submit-by-name', methods=['POST'])
def submit_score_by_name():
    """
    Submit a finished game identified by names (what the browser knows).
    Creates class/subject/skill/game/student/assignment rows on first use,
    then records the score with the same logic as /submit.

    Expected JSON: student, roll, class, subject, skill, game, file,
    responses: [{question_id, user_answer, correct_answer}]
    """
    data = request.json or {}
    if not data.get('responses'):
        return jsonify({'status': 'error', 'message': 'Missing fields: responses'}), 400

    try:
        if data.get('assignment_id'):
            assignment = db.session.get(Assignment, int(data['assignment_id']))
            if not assignment:
                return jsonify({'status': 'error', 'message': 'Assignment not found'}), 404
            if assignment.status == 'completed':
                return jsonify({'status': 'error', 'code': 'already_completed',
                                'message': 'This assignment is already completed.'}), 409
        else:
            required = ['student', 'roll', 'class', 'skill', 'game']
            missing = [f for f in required if not data.get(f)]
            if missing:
                return jsonify({'status': 'error', 'message': f'Missing fields: {", ".join(missing)}'}), 400
            cls = _get_or_create(Class, name=str(data['class'])[:10])
            subject = _get_or_create(Subject, name=data.get('subject') or 'General', class_id=cls.id)
            skill = _get_or_create(Skill, name=data['skill'], subject_id=subject.id,
                                   defaults={'class_id': cls.id})
            game = _get_or_create(Game, name=data['game'][:100],
                                  defaults={'skill_id': skill.id, 'class_id': cls.id,
                                            'file_path': data.get('file')})
            student = _get_or_create(Student, roll_number=str(data['roll'])[:20], class_id=cls.id,
                                     defaults={'name': data['student'][:100]})
            assignment = db.session.query(Assignment).filter_by(
                student_id=student.id, game_id=game.id, status='pending').first()
            if not assignment:
                assignment = Assignment(student_id=student.id, game_id=game.id, class_id=cls.id,
                                        subject_id=subject.id, skill_id=skill.id, status='pending')
                db.session.add(assignment)
                db.session.flush()
        db.session.commit()

        game_score = GameScore(assignment_id=assignment.id, student_id=assignment.student_id,
                               game_id=assignment.game_id, class_id=assignment.class_id,
                               skill_id=assignment.skill_id)
        for r in data['responses']:
            user_answer = str(r.get('user_answer', ''))
            correct_answer = str(r.get('correct_answer', ''))
            game_score.add_response(
                question_id=r.get('question_id'),
                user_answer=user_answer,
                correct_answer=correct_answer,
                is_correct=user_answer.lower() == correct_answer.lower())

        result = game_score.save_to_database()
        if not result['success']:
            return jsonify({'status': 'error', 'message': result['message']}), 500
        return jsonify({'status': 'success', 'score_id': result['score_id'],
                        'score_data': result['score_data']}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# STUDENT PERFORMANCE ENDPOINTS
# ============================================================

@scoring_bp.route('/student/<int:student_id>/performance', methods=['GET'])
def get_student_performance(student_id):
    """Get student's overall performance"""
    try:
        performance = StudentAnalytics.get_student_performance(student_id)

        if not performance:
            return jsonify({
                'status': 'error',
                'message': 'No score data found for this student'
            }), 404

        return jsonify({
            'status': 'success',
            'data': performance
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@scoring_bp.route('/student/<int:student_id>/skill/<int:skill_id>/mastery', methods=['GET'])
def get_skill_mastery(student_id, skill_id):
    """Get student's mastery level for a specific skill"""
    try:
        mastery = StudentAnalytics.get_skill_mastery(student_id, skill_id)

        if not mastery:
            return jsonify({
                'status': 'error',
                'message': 'No score data found for this skill'
            }), 404

        return jsonify({
            'status': 'success',
            'data': mastery
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============================================================
# CLASS PERFORMANCE ENDPOINTS
# ============================================================

@scoring_bp.route('/class/<int:class_id>/performance', methods=['GET'])
def get_class_performance(class_id):
    """Get class-wide performance summary"""
    try:
        performance = StudentAnalytics.get_class_performance(class_id)

        return jsonify({
            'status': 'success',
            'data': performance
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============================================================
# SCORE RETRIEVAL ENDPOINTS
# ============================================================

@scoring_bp.route('/student/<int:student_id>/scores', methods=['GET'])
def get_student_scores(student_id):
    """Get all scores for a student"""
    try:
        scores = db.session.query(Score).filter_by(student_id=student_id).all()

        return jsonify({
            'status': 'success',
            'student_id': student_id,
            'total_scores': len(scores),
            'scores': [s.to_dict() for s in scores]
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@scoring_bp.route('/game/<int:game_id>/scores', methods=['GET'])
def get_game_scores(game_id):
    """Get all scores for a specific game"""
    try:
        scores = db.session.query(Score).filter_by(game_id=game_id).all()

        # Calculate statistics
        if scores:
            avg_percentage = sum(s.percentage for s in scores) / len(scores)
        else:
            avg_percentage = 0

        return jsonify({
            'status': 'success',
            'game_id': game_id,
            'total_attempts': len(scores),
            'average_percentage': round(avg_percentage, 2),
            'scores': [s.to_dict() for s in scores]
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@scoring_bp.route('/score/<int:score_id>', methods=['GET'])
def get_score_details(score_id):
    """Get detailed score information"""
    try:
        score = db.session.query(Score).filter_by(id=score_id).first()

        if not score:
            return jsonify({
                'status': 'error',
                'message': 'Score not found'
            }), 404

        visual_feedback = PerformanceFeedback.get_visual_feedback(score)

        return jsonify({
            'status': 'success',
            'score': score.to_dict(),
            'visual_feedback': visual_feedback
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============================================================
# LEADERBOARD ENDPOINTS
# ============================================================

@scoring_bp.route('/class/<int:class_id>/leaderboard', methods=['GET'])
def get_class_leaderboard(class_id):
    """Get leaderboard for a class (top performers)"""
    try:
        # Get all students in class with their average scores
        students = db.session.query(Student).filter_by(class_id=class_id).all()

        leaderboard = []
        for student in students:
            scores = db.session.query(Score).filter_by(student_id=student.id).all()
            if scores:
                avg_percentage = sum(s.percentage for s in scores) / len(scores)
                total_games = len(scores)

                leaderboard.append({
                    'rank': 0,  # Will be set after sorting
                    'student_id': student.id,
                    'student_name': student.name,
                    'roll_number': student.roll_number,
                    'average_percentage': round(avg_percentage, 2),
                    'total_games': total_games,
                    'total_score': sum(s.score for s in scores)
                })

        # Sort by average percentage (descending)
        leaderboard.sort(key=lambda x: x['average_percentage'], reverse=True)

        # Assign ranks
        for i, entry in enumerate(leaderboard, 1):
            entry['rank'] = i

        return jsonify({
            'status': 'success',
            'class_id': class_id,
            'leaderboard': leaderboard
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@scoring_bp.route('/skill/<int:skill_id>/leaderboard', methods=['GET'])
def get_skill_leaderboard(skill_id):
    """Get leaderboard for a skill (top performers)"""
    try:
        scores = db.session.query(Score).filter_by(skill_id=skill_id).all()

        # Group by student
        student_scores = {}
        for score in scores:
            if score.student_id not in student_scores:
                student_scores[score.student_id] = []
            student_scores[score.student_id].append(score)

        leaderboard = []
        for student_id, scores_list in student_scores.items():
            student = db.session.query(Student).get(student_id)
            if student:
                avg_percentage = sum(s.percentage for s in scores_list) / len(scores_list)

                leaderboard.append({
                    'rank': 0,
                    'student_id': student.id,
                    'student_name': student.name,
                    'average_percentage': round(avg_percentage, 2),
                    'attempts': len(scores_list)
                })

        # Sort by average percentage
        leaderboard.sort(key=lambda x: x['average_percentage'], reverse=True)

        # Assign ranks
        for i, entry in enumerate(leaderboard, 1):
            entry['rank'] = i

        return jsonify({
            'status': 'success',
            'skill_id': skill_id,
            'leaderboard': leaderboard
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
