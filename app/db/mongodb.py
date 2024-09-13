"""MongoDB database connection and initialization."""

from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure
from flask import current_app
import logging

mongo = PyMongo()

def init_db(app):
    """
    Initialize the MongoDB connection.

    Args:
        app (Flask): The Flask application instance.

    Raises:
        ConnectionFailure: If unable to connect to the MongoDB instance.
    """
    mongo.init_app(app)

    try:
        # The ismaster command is cheap and does not require auth.
        mongo.cx.admin.command('ismaster')
        logging.info("MongoDB connection successful.")
    except ConnectionFailure:
        logging.error("MongoDB connection failed.")
        raise

def get_db():
    """
    Get the database connection.

    Returns:
        pymongo.database.Database: The MongoDB database instance.
    """
    return mongo.db