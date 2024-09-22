from app.preprocess.ply_preprocess import PLYProcessor
from app.db.mongodb import get_db
import os
from bson import ObjectId

from app.services.video_service import VideoService


class PreprocessService:
    def __init__(self):
        pass

    @staticmethod
    def process_ply(ply_id):
        """
        Process a PLY file.

        Args:
            ply_id (str): The ID of the PLY file to process.

        Returns:
            dict: The processed PLY file data if found, None otherwise.
        """
        ply_file = VideoService.get_video(ply_id)

        if not ply_file:
            return None

        input_path = ply_file['file_path']

        # Initialize PLY processor
        ply_processor = PLYProcessor(input_path)

        # Remove the background and extract the main object
        ply_processor.preprocess()

        # Save the processed point cloud to the database and a CSV file
        point_cloud_id = ply_processor.save_to_db(name=ply_file['title'])

        # # Update the PLY document with processing information
        # db.ply_files.update_one(
        #     {'_id': ObjectId(ply_id)},
        #     {'$set': {
        #         'processed': True,
        #         'point_cloud_id': point_cloud_id,
        #     }}
        # )

        return {
            'ply_id': ply_id,
            'processed': True,
            'point_cloud_id': point_cloud_id,
        }

    @staticmethod
    def get_progress(ply_id):
        """
        Get the progress of PLY file processing.

        Args:
            ply_id (str): The ID of the PLY file.

        Returns:
            dict: The progress of the PLY file processing if found, None otherwise.
        """
        ply_file = VideoService.get_video(ply_id)

        if not ply_file:
            return None

        if ply_file :
            return {
                'ply_id': ply_id,
                'processed': ply_file.get('processed', False),
                'point_cloud_id': ply_file.get('point_cloud_id', None),
            }
        return None
