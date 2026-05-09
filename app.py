import os
from flask import Flask, render_template, send_from_directory, jsonify
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
        try:
            db.create_all()
        except Exception as e:
            print(f"Database initialization warning: {e}")

    # Try to register blueprints if they exist
    try:
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
    except ImportError as e:
        print(f"Routes not available: {e}")

    # Static routes
    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome to Pandas Assignment API', 'status': 'running'})

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    @app.route('/signup')
    def signup():
        try:
            return send_from_directory('.', 'signup.html')
        except:
            return jsonify({'error': 'signup.html not found'}), 404

    @app.route('/login')
    def login():
        try:
            return send_from_directory('.', 'login.html')
        except:
            return jsonify({'error': 'login.html not found'}), 404

    @app.route('/library')
    def library():
        try:
            return send_from_directory('.', 'library.html')
        except:
            return jsonify({'error': 'library.html not found'}), 404

    @app.route('/assignment/<int:assignment_id>')
    def assignment(assignment_id):
        try:
            return send_from_directory('.', 'assignment.html')
        except:
            return jsonify({'error': 'assignment.html not found'}), 404

    @app.route('/games')
    def games():
        try:
            return send_from_directory('.', 'games.html')
        except:
            return jsonify({'error': 'games.html not found'}), 404

    @app.route('/game-play/<int:game_id>')
    def game_play(game_id):
        try:
            return send_from_directory('.', 'game-play.html')
        except:
            return jsonify({'error': 'game-play.html not found'}), 404

    @app.route('/tournament')
    def tournament():
        try:
            return send_from_directory('.', 'tournament.html')
        except:
            return jsonify({'error': 'tournament.html not found'}), 404

    @app.route('/tournament/<int:tournament_id>')
    def tournament_details(tournament_id):
        try:
            return send_from_directory('.', 'tournament-details.html')
        except:
            return jsonify({'error': 'tournament-details.html not found'}), 404

    @app.route('/profile')
    def profile():
        try:
            return send_from_directory('.', 'profile.html')
        except:
            return jsonify({'error': 'profile.html not found'}), 404

    @app.route('/admin')
    def admin_dashboard():
        try:
            return send_from_directory('.', 'admin-dashboard.html')
        except:
            return jsonify({'error': 'admin-dashboard.html not found'}), 404

    @app.route('/admin/user/<int:user_id>')
    def admin_user_details(user_id):
        try:
            return send_from_directory('.', 'admin-user-details.html')
        except:
            return jsonify({'error': 'admin-user-details.html not found'}), 404

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Internal server error', 'details': str(error)}, 500

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, port=5000)
