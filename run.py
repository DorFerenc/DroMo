"""
Entry point for the DROMO application.

This script creates and runs the Flask application.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)