from app.preprocess.ply_preprocess import PLYProcessor
from app.db.mongodb import get_db
import os
from bson import ObjectId

from app.services.ply_service import PLYService


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
        ply_file = PLYService.get_ply(ply_id)
        if not ply_file:
            return None

        input_path = ply_file['file_path']
        output_dir = os.path.join(os.path.dirname(input_path), f"{ply_id}_processed")

        ply_processor = PLYProcessor()
        points_processed = ply_processor.process(input_path, output_dir)

        if points_processed >= 0:
            # Update PLY file document with processing information
            db = get_db()
            db.ply_files.update_one(
                {'_id': ObjectId(ply_id)},
                {'$set': {
                    'processed': True,
                    'points_processed': points_processed,
                    'output_directory': output_dir
                }}
            )

            return {
                'ply_id': ply_id,
                'points_processed': points_processed,
                'output_directory': output_dir
            }
        return None

    @staticmethod
    def get_progress(ply_id):
        """
        Get the progress of PLY file processing.

        Args:
            ply_id (str): The ID of the PLY file.

        Returns:
            dict: The progress of the PLY file processing if found, None otherwise.
        """
        db = get_db()
        ply_file = db.ply_files.find_one({'_id': ObjectId(ply_id)})

        if ply_file and 'processed' in ply_file:
            return {
                'ply_id': ply_id,
                'points_processed': ply_file.get('points_processed', 0),
                'output_directory': ply_file.get('output_directory', '')
            }
        return None