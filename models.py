"""
Database Models for MyClassboard Games Platform
Using SQLAlchemy ORM with PostgreSQL
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(255))
    level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subjects = db.relationship('Subject', backref='class_obj', lazy=True, cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='class_obj', lazy=True, cascade='all, delete-orphan')
    games = db.relationship('Game', backref='class_obj', lazy=True, cascade='all, delete-orphan')
    students = db.relationship('Student', backref='class_obj', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='class_obj', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='class_obj', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level
        }


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skills = db.relationship('Skill', backref='subject', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('name', 'class_id'),)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'class_id': self.class_id
        }


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Text
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    difficulty_level = db.Column(db.String(20), default='beginner')
    order_index = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    games = db.relationship('Game', backref='skill', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='skill', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('name', 'subject_id'),)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'class_id': self.class_id,
            'difficulty_level': self.difficulty_level
        }


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Text
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    game_type = db.Column(db.String(50))
    file_path = db.Column(db.String(255))
    difficulty_level = db.Column(db.String(20), default='beginner')
    max_score = db.Column(db.Integer, default=50)
    questions_count = db.Column(db.Integer, default=5)
    duration_minutes = db.Column(db.Integer, default=5)
    icon = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='game', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'skill_id': self.skill_id,
            'class_id': self.class_id,
            'game_type': self.game_type,
            'file_path': self.file_path,
            'difficulty_level': self.difficulty_level,
            'max_score': self.max_score,
            'available': self.file_path is not None
        }


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='SET NULL'))
    department = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='teacher', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'class_id': self.class_id
        }


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='student', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='student', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('roll_number', 'class_id'),)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'roll': self.roll_number,
            'class_id': self.class_id,
            'email': self.email
        }


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'))
    assigned_by = db.Column(db.String(100))
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    is_mandatory = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject = db.relationship('Subject', backref='assignments')
    scores = db.relationship('Score', backref='assignment', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'game_id': self.game_id,
            'class_id': self.class_id,
            'subject_id': self.subject_id,
            'skill_id': self.skill_id,
            'status': self.status,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None
        }


class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id', ondelete='CASCADE'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'))
    game_id = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'))
    student_name = db.Column(db.String(100))
    student_roll = db.Column(db.String(20))
    game_name = db.Column(db.String(200))
    game_type = db.Column(db.String(50))
    pin_id = db.Column(db.Integer, db.ForeignKey('game_pins.id', ondelete='SET NULL'))
    score = db.Column(db.Integer, default=0)
    max_score = db.Column(db.Integer, default=50)
    percentage = db.Column(db.Numeric(5, 2))
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=5)
    completion_time = db.Column(db.Integer)
    performance_level = db.Column(db.String(20))
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'game_id': self.game_id,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': float(self.percentage) if self.percentage else 0,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id', ondelete='CASCADE'))
    games_played = db.Column(db.Integer, default=0)
    games_completed = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Numeric(5, 2))
    total_time_spent = db.Column(db.Integer)
    last_played = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'games_played': self.games_played,
            'average_score': float(self.average_score) if self.average_score else 0
        }


class ApiLog(db.Model):
    __tablename__ = 'api_logs'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='SET NULL'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Text
    error_message = db.Text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SystemSettings(db.Model):
    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Text
    setting_type = db.Column(db.String(50))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AudioFeedback(db.Model):
    __tablename__ = 'audio_feedback'

    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('scores.id', ondelete='CASCADE'), nullable=False)
    feedback_type = db.Column(db.String(20))
    frequency = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    is_played = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    score = db.relationship('Score', backref='audio_feedback')


class GamePin(db.Model):
    __tablename__ = 'game_pins'

    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(6), unique=True, nullable=False, index=True)
    game_id = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(200), nullable=False)
    game_type = db.Column(db.String(50))
    game_class = db.Column(db.String(10))
    game_subject = db.Column(db.String(100))
    game_skill = db.Column(db.String(100))
    game_subskill = db.Column(db.String(100))
    is_approved = db.Column(db.Boolean, default=True)
    teacher_name = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    use_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'pin': self.pin,
            'game_id': self.game_id,
            'game_name': self.game_name,
            'game_type': self.game_type,
            'game_class': self.game_class,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CachedAiTask(db.Model):
    __tablename__ = 'cached_ai_tasks'

    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    class_name = db.Column(db.String(10), nullable=False, index=True)
    subject = db.Column(db.String(50), nullable=False, index=True)
    topic = db.Column(db.String(150), nullable=False, index=True)
    difficulty = db.Column(db.String(20), default='Medium')
    num_questions = db.Column(db.Integer, default=3)
    task_data = db.Column(db.Text, nullable=False)  # JSON-encoded string for maximum compatibility
    provider = db.Column(db.String(100), default='Gemini')
    hit_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        try:
            parsed_data = json.loads(self.task_data) if isinstance(self.task_data, str) else self.task_data
        except Exception:
            parsed_data = {}
        return {
            'id': self.id,
            'cache_key': self.cache_key,
            'class': self.class_name,
            'subject': self.subject,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'num_questions': self.num_questions,
            'task': parsed_data,
            'provider': self.provider,
            'hit_count': self.hit_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
