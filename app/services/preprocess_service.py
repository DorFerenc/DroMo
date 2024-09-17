from app.preprocess.videos_to_frames import FrameExtractor
from app.db.mongodb import get_db
import os
from bson import ObjectId

from app.services.video_service import VideoService


class PreprocessService:
    def __init__(self):
        pass

    @staticmethod
    def process_video(video_id):
        """
               Process a video.
                Args:
                    video_id (str): The ID of the video to process.
                Returns:
                    dict: The processed video data if found, None otherwise.
                """
        video = VideoService.get_video(video_id)
        if not video:
            return None

        input_path = video['file_path']
        output_dir = os.path.join(os.path.dirname(input_path), f"{video_id}_frames")

        frameExtractor = FrameExtractor()
        frames_processed = frameExtractor.extract_relevant_frames(input_path, output_dir)

        if frames_processed >= 0:
            # Update video document with processing information
            db = get_db()
            db.videos.update_one(
                {'_id': ObjectId(video_id)},
                {'$set': {
                    'processed': True,
                    'frames_processed': frames_processed,
                    'frames_directory': output_dir
                }}
            )

            return {
                'video_id': video_id,
                'frames_processed': frames_processed,
                'frames_directory': output_dir
            }
        return None

    @staticmethod
    def get_progress(video_id):
        """
        Get the progress of video processing.
        Args:
            video_id (str): The ID of the video.
        Returns:
            dict: The progress of the video processing if found, None otherwise.
        """
        db = get_db()
        video = db.videos.find_one({'_id': ObjectId(video_id)})

        if video and 'processed' in video:
            return {
                'video_id': video_id,
                'frames_processed': video.get('frames_processed', 0),
                'frames_directory': video.get('frames_directory', '')
            }
        return None