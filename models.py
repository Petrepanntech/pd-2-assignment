from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_instructor = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    submissions = db.relationship('Submission', backref='user', lazy=True, cascade='all, delete-orphan')
    user_progress = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    game_attempts = db.relationship('GameAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    tournament_participants = db.relationship('TournamentParticipant', backref='user', lazy=True, cascade='all, delete-orphan')
    user_profile = db.relationship('UserProfile', backref='user', lazy=False, uselist=False, cascade='all, delete-orphan')

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    avatar = db.Column(db.String(255), default=None)
    bio = db.Column(db.Text, default='')
    total_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    badges = db.Column(db.String(500), default='')

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    icon = db.Column(db.String(50), default='📚')
    difficulty = db.Column(db.String(50), default='beginner')
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='course', lazy=True, cascade='all, delete-orphan')

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    questions = db.Column(db.JSON, default={})
    dataset_file = db.Column(db.String(255), default=None)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_progress = db.relationship('UserProgress', backref='assignment', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False, index=True)
    progress_pct = db.Column(db.Integer, default=0)
    completed_tasks = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=None)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'assignment_id', name='uq_user_assignment'),)

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    game_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), default='intermediate')
    category = db.Column(db.String(100), nullable=False, index=True)
    icon = db.Column(db.String(50), default='🎮')
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    game_attempts = db.relationship('GameAttempt', backref='game', lazy=True, cascade='all, delete-orphan')

class GameAttempt(db.Model):
    __tablename__ = 'game_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, default='')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    participants = db.relationship('TournamentParticipant', backref='tournament', lazy=True, cascade='all, delete-orphan')

class TournamentParticipant(db.Model):
    __tablename__ = 'tournament_participants'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rank = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('tournament_id', 'user_id', name='uq_tournament_user'),)

class TaskProgress(db.Model):
    __tablename__ = 'task_progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False, index=True)
    task_id = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)