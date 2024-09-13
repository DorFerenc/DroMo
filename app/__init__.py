"""Main application module."""

from flask import Flask
from app.config import Config
from app.db.mongodb import init_db
from app.api.routes import api_bp
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

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

    # Register blueprints
    app.register_blueprint(api_bp)

    return app