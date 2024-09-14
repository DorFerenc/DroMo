"""Service layer for video-related operations."""

from app.models.video import Video
from bson import ObjectId
from bson.errors import InvalidId
from app.db.mongodb import get_db

class VideoService:
    """Handles business logic for video operations."""

    @staticmethod
    def create_video(title, file_path):
        """
        Create a new video entry.

        Args:
            title (str): The title of the video.
            file_path (str): The path where the video file is stored.

        Returns:
            str: The ID of the created video.
        """
        video = Video(title=title, file_path=file_path)
        return video.save()

    @staticmethod
    def get_video(video_id):
        """
        Retrieve a video by its ID.

        Args:
            video_id (str): The ID of the video to retrieve.

        Returns:
            dict: The video data if found, None otherwise.
        """
        try:
            return Video.get_by_id(video_id)
        except InvalidId:
            return None
        # return Video.get_by_id(video_id)

    @staticmethod
    def get_all_videos():
        """Retrieve all videos."""
        db = get_db()
        return list(db.videos.find())

    @staticmethod
    def delete_video(video_id):
        """Delete a video by its ID."""
        try:
            db = get_db()
            result = db.videos.delete_one({'_id': ObjectId(video_id)})
            return result.deleted_count > 0
        except InvalidId:
            return False