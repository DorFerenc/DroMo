from app.preprocess.ply_preprocess import PLYProcessor
from app.db.mongodb import get_db
import os
from bson import ObjectId

from app.services.visual_data_service import VisualDataService


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
        ply_file = VisualDataService.get_visual_data(ply_id)

        if not ply_file:
            return None

        input_path = ply_file['file_path']

        # Initialize PLY processor
        ply_processor = PLYProcessor(input_path, ply_id)

        # Remove the background and extract the main object
        # ply_processor.preprocess()
        distance_threshold = 0.015
        ransac_n = 3
        num_iterations = 1000
        cluster_eps = 0.02
        min_points = 50

        #load the pointCloud
        pcd = ply_processor.load_point_cloud()
        ply_processor.main_object = pcd

        # Center the point cloud
        center_pcd = ply_processor.center_point_cloud(pcd)

        # Remove statistical outliers
        filtered_pcd = ply_processor.remove_statistical_outliers(center_pcd)

        # Voxel downsampling
        filtered_pcd = ply_processor.voxel_downsample(filtered_pcd)

        # Estimate normals
        filtered_pcd = ply_processor.estimate_normals(filtered_pcd)

        # Plane segmention
        remaining_cloud = ply_processor.segment_plane(filtered_pcd, distance_threshold, ransac_n, num_iterations)

        #clustering
        main_object = ply_processor.cluster_points(remaining_cloud, cluster_eps, min_points)

        # Remove statistical outliers, Center the point cloud, and Estimate normals again
        main_object = ply_processor.remove_statistical_outliers(main_object, nn =30, std_multiplier=2.0)
        main_object = ply_processor.center_point_cloud(main_object)
        main_object = ply_processor.estimate_normals(main_object, max_nn=16)
        ply_processor.main_object = main_object

        # Object bottom completion
        complete_object = ply_processor.complete_bottom(main_object)

        # Final object center
        complete_object = ply_processor.center_point_cloud(complete_object)
        ply_processor.main_object = complete_object



        # Save the processed point cloud to the database and a CSV file
        point_cloud_id = ply_processor.save_to_db(name=ply_file['title'])
        ply_processor.save_ply_file_system(pcd, title="original_ply", id=point_cloud_id)
        ply_processor.save_ply_file_system(filtered_pcd, title="filtered_ply", id=point_cloud_id)
        ply_processor.save_ply_file_system(main_object, title="removed_background_ply", id=point_cloud_id)
        ply_processor.save_ply_file_system(complete_object, title="complete_object_ply", id=point_cloud_id)

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
        ply_file = VisualDataService.get_visual_data(ply_id)

        if not ply_file:
            return None

        if ply_file :
            return {
                'ply_id': ply_id,
                'processed': ply_file.get('processed', False),
                'point_cloud_id': ply_file.get('point_cloud_id', None),
            }
        return None


    def get_ply(self, ply_id, param):
        temp_PLY_Processor = PLYProcessor(None, ply_id)
        ply = temp_PLY_Processor.get_ply(param)
        if ply is not None:
            ply = temp_PLY_Processor.format_point_cloud_to_serializable(ply)
        return ply
