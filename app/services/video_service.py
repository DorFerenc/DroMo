"""Service layer for video-related operations."""

from app.models.video import Video

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
        return Video.get_by_id(video_id)