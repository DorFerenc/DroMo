"""MongoDB database connection and initialization."""

from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure
from flask import current_app, g
import logging

mongo = PyMongo()
logger = logging.getLogger(__name__)


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
        # Test the connection
        mongo.db.command('ping')
        logger.info("Successfully connected to MongoDB")
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