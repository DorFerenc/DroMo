"""PLY model for representing and interacting with .ply file data."""

from datetime import datetime
from bson import ObjectId
from app.db.mongodb import get_db

class PLYFile:
    """Represents a PLY file in the system."""

    def __init__(self, title, file_path):
        """
        Initialize a new PLYFile instance.

        Args:
            title (str): The title of the .ply file.
            file_path (str): The path where the .ply file is stored.
        """
        self.title = title
        self.file_path = file_path
        self.timestamp = datetime.utcnow()

    def save(self):
        """
        Save the PLY file to the database.

        Returns:
            str: The ID of the inserted PLY file document.
        """
        db = get_db()
        result = db.ply_files.insert_one({
            'title': self.title,
            'file_path': self.file_path,
            'timestamp': self.timestamp
        })
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(ply_id):
        """
        Retrieve a PLY file by its ID.

        Args:
            ply_id (str): The ID of the PLY file to retrieve.

        Returns:
            dict: The PLY file document if found, None otherwise.
        """
        db = get_db()
        return db.ply_files.find_one({'_id': ObjectId(ply_id)})
