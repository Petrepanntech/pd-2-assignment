import os
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from config import config
from models import db

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='.', static_url_path='')
    CORS(app)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.courses import courses_bp
    from routes.games import games_bp
    from routes.tournaments import tournaments_bp
    from routes.admin import admin_bp
    from routes.search import search_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(games_bp, url_prefix='/api/games')
    app.register_blueprint(tournaments_bp, url_prefix='/api/tournaments')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(search_bp, url_prefix='/api/search')

    # Static routes
    @app.route('/')
    def home():
        return send_from_directory('.', 'home.html')

    @app.route('/signup')
    def signup():
        return send_from_directory('.', 'signup.html')

    @app.route('/login')
    def login():
        return send_from_directory('.', 'login.html')

    @app.route('/library')
    def library():
        return send_from_directory('.', 'library.html')

    @app.route('/assignment/<int:assignment_id>')
    def assignment(assignment_id):
        return send_from_directory('.', 'assignment.html')

    @app.route('/games')
    def games():
        return send_from_directory('.', 'games.html')

    @app.route('/game-play/<int:game_id>')
    def game_play(game_id):
        return send_from_directory('.', 'game-play.html')

    @app.route('/tournament')
    def tournament():
        return send_from_directory('.', 'tournament.html')

    @app.route('/tournament/<int:tournament_id>')
    def tournament_details(tournament_id):
        return send_from_directory('.', 'tournament-details.html')

    @app.route('/profile')
    def profile():
        return send_from_directory('.', 'profile.html')

    @app.route('/admin')
    def admin_dashboard():
        return send_from_directory('.', 'admin-dashboard.html')

    @app.route('/admin/user/<int:user_id>')
    def admin_user_details(user_id):
        return send_from_directory('.', 'admin-user-details.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Internal server error'}, 500

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, port=5000)