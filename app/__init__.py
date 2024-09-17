"""Main application module."""
from flask import Flask, send_from_directory
from app.config import Config
from app.db.mongodb import init_db
from app.api.routes import api_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging


load_dotenv()  # Load environment variables from .env file

# Create logs directory if it doesn't exist
os.makedirs('/app/logs', exist_ok=True)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log')

# Add a stream handler to also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class (default: Config)

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_db(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app