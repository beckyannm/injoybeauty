"""
Jamie's Beauty Studio - Flask Application
Main entry point for the backend API.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from database import init_db, seed_services, seed_gallery

# Import route blueprints
from routes.bookings import bookings_bp
from routes.contact import contact_bp
from routes.gallery import gallery_bp
from routes.services import services_bp
from routes.intake import intake_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                static_folder='../frontend',
                static_url_path='')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(bookings_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(intake_bp)
    
    # Serve frontend pages
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:filename>')
    def serve_static(filename):
        # Check if file exists, otherwise serve index.html for SPA-like behavior
        file_path = Path(app.static_folder) / filename
        if file_path.exists():
            return send_from_directory(app.static_folder, filename)
        # If it's an HTML page request, try to find it
        if not '.' in filename:
            html_file = f"{filename}.html"
            html_path = Path(app.static_folder) / html_file
            if html_path.exists():
                return send_from_directory(app.static_folder, html_file)
        return send_from_directory(app.static_folder, 'index.html')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'business': Config.BUSINESS_NAME
        })
    
    # Lazy database initialization (non-blocking startup)
    # Database will be initialized on first request instead of at app startup
    @app.before_request
    def ensure_db_initialized():
        """Initialize database on first request (lazy loading)."""
        if not hasattr(app, '_db_initialized'):
            try:
                init_db()
                seed_services()
                seed_gallery()
                app._db_initialized = True
                print("Database initialized on first request.")
            except Exception as e:
                print(f"Database initialization error: {e}")
    
    return app


# Initialize database and seed data (for local development)
def setup_database():
    """Initialize database with tables and seed data."""
    print("Setting up database...")
    init_db()
    seed_services()
    seed_gallery()


# Create app instance for gunicorn (must be at module level)
app = create_app()

if __name__ == '__main__':
    # Setup database
    setup_database()
    
    # Create and run app
    print(f"\n{'='*50}")
    print(f"  {Config.BUSINESS_NAME}")
    print(f"  Server running at http://localhost:5000")
    print(f"{'='*50}\n")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
