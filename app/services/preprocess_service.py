from app.preprocess.videos_to_frames import FrameExtractor
from app.db.mongodb import get_db
import os
from bson import ObjectId



class PreprocessService:
    def __init__(self):
        self.frameExtractor = FrameExtractor()


    @staticmethod
    def process_video(self, video_id):
        """
               Process a video.
                Args:
                    video_id (str): The ID of the video to process.
                Returns:
                    dict: The processed video data if found, None otherwise.
                """
        video = self.get_video(video_id)
        if not video:
            return None

        input_path = video['file_path']
        output_dir = os.path.join(os.path.dirname(input_path), f"{video_id}_frames")

        frames_processed = self.frameExtractor.extract_relevant_frames(input_path, output_dir)

        if frames_processed > 0:
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
    def get_progress(self, video_id):
        pass