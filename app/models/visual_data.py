"""visual_data model for representing and interacting with visual_data data."""

from datetime import datetime
from bson import ObjectId
from app.db.mongodb import get_db

class VisualData:
    """Represents a visual_data in the system."""

    def __init__(self, title, file_path):
        """
        Initialize a new visual data instance.

        Args:
            title (str): The title of the visual data.
            file_path (str): The path where the visual data file is stored.
        """
        self.title = title
        self.file_path = file_path
        self.timestamp = datetime.utcnow()

    def save(self):
        """
        Save the visual data to the database.

        Returns:
            str: The ID of the inserted visual data document.
        """
        db = get_db()
        result = db.visual_datas.insert_one({
            'title': self.title,
            'file_path': self.file_path,
            'timestamp': self.timestamp
        })
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(visual_data_id):
        """
        Retrieve a visual_data by its ID.

        Args:
            visual_data_id (str): The ID of the visual data to retrieve.

        Returns:
            dict: The visual data document if found, None otherwise.
        """
        db = get_db()
        return db.visual_datas.find_one({'_id': ObjectId(visual_data_id)})