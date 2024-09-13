"""Video model for representing and interacting with video data."""

from datetime import datetime
from bson import ObjectId
from app.db.mongodb import get_db

class Video:
    """Represents a video in the system."""

    def __init__(self, title, file_path):
        """
        Initialize a new Video instance.

        Args:
            title (str): The title of the video.
            file_path (str): The path where the video file is stored.
        """
        self.title = title
        self.file_path = file_path
        self.timestamp = datetime.utcnow()

    def save(self):
        """
        Save the video to the database.

        Returns:
            str: The ID of the inserted video document.
        """
        db = get_db()
        result = db.videos.insert_one({
            'title': self.title,
            'file_path': self.file_path,
            'timestamp': self.timestamp
        })
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(video_id):
        """
        Retrieve a video by its ID.

        Args:
            video_id (str): The ID of the video to retrieve.

        Returns:
            dict: The video document if found, None otherwise.
        """
        db = get_db()
        return db.videos.find_one({'_id': ObjectId(video_id)})