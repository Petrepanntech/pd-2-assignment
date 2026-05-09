import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, get_config_name

# Create Flask app for Vercel
app = create_app(get_config_name(default='production'))
