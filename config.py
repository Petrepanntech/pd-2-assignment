import os
from datetime import timedelta


def _normalize_database_url(database_url):
    if database_url.startswith('postgres://'):
        return database_url.replace('postgres://', 'postgresql://', 1)
    return database_url


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'dev-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    @staticmethod
    def init_app(app):
        app.config['SQLALCHEMY_DATABASE_URI'] = _normalize_database_url(
            os.getenv('DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])
        )
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['JWT_SECRET_KEY'])
        app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', app.config['UPLOAD_FOLDER'])
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        Config.init_app(app)

        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret or jwt_secret == 'dev-secret-key-change-in-production':
            raise RuntimeError('JWT_SECRET_KEY environment variable is required in production')

        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            raise RuntimeError('DATABASE_URL must point to a persistent database in production')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
