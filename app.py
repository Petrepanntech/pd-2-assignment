import os
import importlib
import importlib.util
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import config
from models import db

BASE_DIR = Path(__file__).resolve().parent


def get_config_name(default='development'):
    env_name = (os.getenv('APP_ENV') or os.getenv('FLASK_ENV') or default).lower()
    if env_name in config:
        return env_name
    return default


def create_app(config_name='development'):
    app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path='')
    CORS(app)

    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    blueprints = [
        ('routes.auth', 'auth_bp', '/api/auth'),
        ('routes.courses', 'courses_bp', '/api/courses'),
        ('routes.games', 'games_bp', '/api/games'),
        ('routes.tournaments', 'tournaments_bp', '/api/tournaments'),
        ('routes.admin', 'admin_bp', '/api/admin'),
        ('routes.search', 'search_bp', '/api/search'),
    ]

    for module_name, blueprint_name, url_prefix in blueprints:
        try:
            module_spec = importlib.util.find_spec(module_name)
        except ModuleNotFoundError:
            module_spec = None
        if module_spec is None:
            continue
        module = importlib.import_module(module_name)
        app.register_blueprint(getattr(module, blueprint_name), url_prefix=url_prefix)

    should_create_tables = (
        app.config.get('TESTING', False)
        or app.config.get('DEBUG', False)
        or os.getenv('RUN_DB_CREATE_ALL', 'false').lower() == 'true'
    )
    if should_create_tables:
        with app.app_context():
            db.create_all()

    static_roots = [BASE_DIR, BASE_DIR / 'templates']

    def serve_page(filename):
        for root in static_roots:
            if (root / filename).exists():
                return send_from_directory(str(root), filename)
        return {'error': f'Page "{filename}" was not found in deployment artifact'}, 404

    # Static routes
    @app.route('/')
    def home():
        return serve_page('home.html')

    @app.route('/signup')
    def signup():
        return serve_page('signup.html')

    @app.route('/login')
    def login():
        return serve_page('login.html')

    @app.route('/library')
    def library():
        return serve_page('library.html')

    @app.route('/assignment/<int:assignment_id>')
    def assignment(assignment_id):
        return serve_page('assignment.html')

    @app.route('/games')
    def games():
        return serve_page('games.html')

    @app.route('/game-play/<int:game_id>')
    def game_play(game_id):
        return serve_page('game-play.html')

    @app.route('/tournament')
    def tournament():
        return serve_page('tournament.html')

    @app.route('/tournament/<int:tournament_id>')
    def tournament_details(tournament_id):
        return serve_page('tournament-details.html')

    @app.route('/profile')
    def profile():
        return serve_page('profile.html')

    @app.route('/admin')
    def admin_dashboard():
        return serve_page('admin-dashboard.html')

    @app.route('/admin/user/<int:user_id>')
    def admin_user_details(user_id):
        return serve_page('admin-user-details.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Internal server error'}, 500

    @app.cli.command('init-db')
    def init_db_command():
        with app.app_context():
            db.create_all()
        print('Database initialized.')

    return app

if __name__ == '__main__':
    app = create_app(get_config_name())
    app.run(debug=app.config.get('DEBUG', False), port=5000)
