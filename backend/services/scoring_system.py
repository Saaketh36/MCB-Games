#!/usr/bin/env python3
"""
Scoring System for MyClassboard Games
Tracks student performance, correct/incorrect answers, and provides feedback
"""

from backend.models import db, Score, Assignment, Student, Game, Skill
from datetime import datetime
from sqlalchemy import func

class GameScore:
    """Manages scoring for game submissions"""

    def __init__(self, assignment_id, student_id, game_id, class_id, skill_id):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.game_id = game_id
        self.class_id = class_id
        self.skill_id = skill_id
        self.responses = []
        self.start_time = datetime.utcnow()

    def add_response(self, question_id, user_answer, correct_answer, is_correct):
        """Record a response"""
        self.responses.append({
            'question_id': question_id,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'timestamp': datetime.utcnow()
        })

    def calculate_score(self):
        """Calculate final score"""
        total_questions = len(self.responses)
        correct_answers = sum(1 for r in self.responses if r['is_correct'])
        wrong_answers = total_questions - correct_answers

        # Calculate percentage (each question worth 10 points out of 100)
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        # Determine performance level
        if percentage >= 80:
            performance_level = 'excellent'
        elif percentage >= 60:
            performance_level = 'good'
        elif percentage >= 40:
            performance_level = 'average'
        else:
            performance_level = 'poor'

        return {
            'score': correct_answers * 10,  # Each correct answer = 10 points
            'max_score': total_questions * 10,
            'percentage': percentage,
            'correct_answers': correct_answers,
            'wrong_answers': wrong_answers,
            'total_questions': total_questions,
            'performance_level': performance_level
        }

    def save_to_database(self):
        """Save score to database"""
        try:
            score_data = self.calculate_score()
            completion_time = (datetime.utcnow() - self.start_time).total_seconds()

            score = Score(
                assignment_id=self.assignment_id,
                student_id=self.student_id,
                game_id=self.game_id,
                class_id=self.class_id,
                skill_id=self.skill_id,
                score=score_data['score'],
                max_score=score_data['max_score'],
                percentage=score_data['percentage'],
                correct_answers=score_data['correct_answers'],
                wrong_answers=score_data['wrong_answers'],
                total_questions=score_data['total_questions'],
                performance_level=score_data['performance_level'],
                completion_time=int(completion_time),
                completed_at=datetime.utcnow()
            )

            db.session.add(score)
            db.session.commit()

            # Update assignment status
            assignment = Assignment.query.get(self.assignment_id)
            if assignment:
                assignment.status = 'completed'
                db.session.commit()

            return {
                'success': True,
                'score_id': score.id,
                'score_data': score_data,
                'message': 'Score saved successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to save score'
            }

class StudentAnalytics:
    """Analyzes student performance"""

    @staticmethod
    def get_student_performance(student_id):
        """Get overall student performance"""
        scores = db.session.query(Score).filter_by(student_id=student_id).all()

        if not scores:
            return None

        total_games = len(scores)
        total_score = sum(s.score for s in scores)
        average_percentage = sum(s.percentage for s in scores) / total_games

        # Count by performance level
        excellent = len([s for s in scores if s.performance_level == 'excellent'])
        good = len([s for s in scores if s.performance_level == 'good'])
        average = len([s for s in scores if s.performance_level == 'average'])
        poor = len([s for s in scores if s.performance_level == 'poor'])

        return {
            'student_id': student_id,
            'total_games_played': total_games,
            'total_score': total_score,
            'average_percentage': round(average_percentage, 2),
            'performance_breakdown': {
                'excellent': excellent,
                'good': good,
                'average': average,
                'poor': poor
            },
            'scores': [s.to_dict() for s in scores]
        }

    @staticmethod
    def get_class_performance(class_id):
        """Get class-wide performance"""
        students = db.session.query(Student).filter_by(class_id=class_id).all()

        class_stats = {
            'class_id': class_id,
            'total_students': len(students),
            'students_data': []
        }

        for student in students:
            perf = StudentAnalytics.get_student_performance(student.id)
            if perf:
                class_stats['students_data'].append(perf)

        return class_stats

    @staticmethod
    def get_skill_mastery(student_id, skill_id):
        """Get student mastery level for a skill"""
        scores = db.session.query(Score).filter_by(
            student_id=student_id,
            skill_id=skill_id
        ).all()

        if not scores:
            return None

        percentages = [s.percentage for s in scores]
        average = sum(percentages) / len(percentages)

        # Mastery level
        if average >= 80:
            mastery = 'Mastered'
        elif average >= 60:
            mastery = 'Proficient'
        elif average >= 40:
            mastery = 'Developing'
        else:
            mastery = 'Beginning'

        return {
            'student_id': student_id,
            'skill_id': skill_id,
            'attempts': len(scores),
            'average_percentage': round(average, 2),
            'mastery_level': mastery,
            'scores': [s.to_dict() for s in scores]
        }

class PerformanceFeedback:
    """Generates visual feedback for students"""

    @staticmethod
    def get_visual_feedback(score_obj):
        """Generate visual feedback based on score"""
        percentage = score_obj.percentage
        performance = score_obj.performance_level

        # Visual indicators
        if performance == 'excellent':
            emoji = '🎉'
            message = 'Excellent! Outstanding performance!'
            color = 'green'
            stars = '⭐⭐⭐⭐⭐'
        elif performance == 'good':
            emoji = '👏'
            message = 'Great job! Good performance!'
            color = 'lightgreen'
            stars = '⭐⭐⭐⭐'
        elif performance == 'average':
            emoji = '👍'
            message = 'Good effort! Keep practicing!'
            color = 'yellow'
            stars = '⭐⭐⭐'
        else:
            emoji = '💪'
            message = 'Keep trying! You can do better!'
            color = 'orange'
            stars = '⭐⭐'

        return {
            'emoji': emoji,
            'message': message,
            'color': color,
            'stars': stars,
            'percentage': percentage,
            'performance_level': performance,
            'correct': score_obj.correct_answers,
            'wrong': score_obj.wrong_answers,
            'total': score_obj.total_questions
        }

    @staticmethod
    def get_answer_feedback(is_correct, user_answer, correct_answer):
        """Get feedback for individual answer"""
        if is_correct:
            return {
                'status': '✅ CORRECT',
                'emoji': '✅',
                'message': 'Great!',
                'color': 'green',
                'sound': 'correct'
            }
        else:
            return {
                'status': '❌ WRONG',
                'emoji': '❌',
                'message': f'Correct answer: {correct_answer}',
                'color': 'red',
                'sound': 'wrong'
            }
