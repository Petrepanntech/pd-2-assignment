import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create Flask app for Vercel
app = create_app(os.getenv('FLASK_ENV', 'production'))

# Vercel requires WSGI app export
def handler(request):
    """WSGI handler for Vercel"""
    with app.app_context():
        return app.wsgi_app
