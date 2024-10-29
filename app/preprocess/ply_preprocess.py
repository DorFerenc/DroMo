import logging

import open3d as o3d
import numpy as np
import os

from app.models.point_cloud import PointCloud
from app.services.recon_proc_visualization_service import ReconProcVisualizationService


class PLYProcessor:
    """Handles operations related to processing and saving PLY files."""

    def __init__(self, ply_file, ply_id):
        self.ply_file = ply_file
        self.main_object = None
        self.ply_id = ply_id

    def preprocess(self, distance_threshold=0.015, ransac_n=3, num_iterations=1000, cluster_eps=0.02,
                          min_points=50):
        """
        Remove the background from a point cloud file and extract the main object.
        """
        pcd = self.load_point_cloud()
        self.main_object = pcd
        # Center the point cloud
        center_pcd = self.center_point_cloud(pcd)
        # Remove statistical outliers
        filtered_pcd = self.remove_statistical_outliers(center_pcd)
        # Voxel downsampling
        filtered_pcd = self.voxel_downsample(filtered_pcd)
        # Estimate normals
        filtered_pcd = self.estimate_normals(filtered_pcd)
        #
        remaining_cloud = self.segment_plane(filtered_pcd, distance_threshold, ransac_n, num_iterations)
        # remaining_cloud = self.get_remaining_cloud()
        #
        main_object = self.cluster_points(remaining_cloud, cluster_eps, min_points)
        #
        main_object = self.remove_statistical_outliers(main_object, nn =30, std_multiplier=2.0)
        main_object = self.center_point_cloud(main_object)
        main_object = self.estimate_normals(main_object, max_nn=16)
        self.main_object = main_object

        main_object, bottom = self.complete_bottom(main_object)

        main_object = self.center_point_cloud(main_object)
        self.main_object = main_object
        return main_object, bottom


    def load_point_cloud(self):
        """Load the point cloud from the PLY file."""
        logging.info("Loading point cloud from file.")
        pcd = o3d.io.read_point_cloud(self.ply_file)
        logging.info("Point cloud loaded successfully.")
        return pcd
    def center_point_cloud(self, pcd):
        pcd_center = pcd.get_center()
        pcd.translate(-pcd_center)
        return pcd
    def remove_statistical_outliers(self, pcd, nn=16, std_multiplier=10):
        """
        Remove statistical outliers from the point cloud.
        :param pcd: Input point cloud.
        :param nn: Number of nearest neighbors to consider.
        :param std_multiplier: Standard deviation multiplier.
        :return: Filtered point cloud and outlier indices.
        """
        filtered_pcd, inlier_indices = pcd.remove_statistical_outlier(nn, std_multiplier)
        outliers = pcd.select_by_index(inlier_indices, invert=True)

        # Log the number of outliers removed
        logging.info(f"Removed {len(outliers.points)} outliers from the point cloud.")

        return filtered_pcd

    def voxel_downsample(self, pcd, voxel_size=0.002):
        """
        Downsample the point cloud using a voxel grid filter.
        :param pcd: Input point cloud.
        :param voxel_size: Size of the voxel grid.
        :return: Downsampled point cloud.
        """
        downsampled_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
        logging.info(f"Downsampled point cloud from {len(pcd.points)} to {len(downsampled_pcd.points)} points.")

        return downsampled_pcd

    def estimate_normals(self, pcd, max_nn=30):
        """
        Estimate normals for the point cloud.
        :param pcd: Input point cloud.
        :return: Point cloud with estimated normals.
        """
        nn_distance = np.mean(pcd.compute_nearest_neighbor_distance())
        radius_normals = nn_distance * 10
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normals, max_nn=max_nn),
            fast_normal_computation=True
        )
        logging.info("Normals estimated for the point cloud.")

        return pcd
    def segment_plane(self, pcd, distance_threshold, ransac_n, num_iterations):
        """Segment the largest plane from the point cloud."""
        points = np.asarray(pcd.points)
        z_min = np.min(points[:, 1])  # Min z value (ground level)
        z_max = np.max(points[:, 1])  # Max z value (top of the object)
        object_height = z_max - z_min
        min_height = 0.03
        max_height = 0.2
        distance_threshold = np.interp(object_height, [min_height, max_height], [0.006, 0.03])

        logging.info("Segmenting the largest plane from the point cloud.")
        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                 ransac_n=ransac_n,
                                                 num_iterations=num_iterations)
        logging.info("Plane segmentation completed.")
        return pcd.select_by_index(inliers, invert=True)

    def get_remaining_cloud(self):
        """Return the remaining cloud (non-plane points) after plane segmentation."""
        logging.info("Extracting remaining points from the point cloud.")
        return self.main_object

    def cluster_points(self, remaining_cloud, cluster_eps, min_points):
        """Cluster remaining points to find the main object."""
        logging.info("Clustering remaining points.")
        labels = np.array(remaining_cloud.cluster_dbscan(eps=cluster_eps, min_points=min_points))

        if len(labels) == 0:
            logging.warning("Clustering failed. Returning all non-plane points.")
            return remaining_cloud


        # Find the largest cluster (assumed to be the main object)
        max_label = labels.max()
        logging.info(f"Point cloud has {max_label + 1} clusters")
        cluster_sizes = [len(labels[labels == i]) for i in range(max_label + 1)]
        largest_cluster = np.argmax(cluster_sizes)

        # Extract the largest cluster
        main_object = remaining_cloud.select_by_index(np.where(labels == largest_cluster)[0])
        logging.info("Largest cluster extracted successfully.")
        return main_object

    def complete_bottom(self, pcd, resolution=0.005, depth=0.005):
        """Complete the bottom of the object."""
        logging.info("Completing the bottom of the object.")
        hull = self.compute_convex_hull(pcd)
        outer_shape_pcd = self.sample_hull_surface(hull)
        bottom_surface_points = self.extract_bottom_surface(outer_shape_pcd, depth)
        bottom_surface_pcd = self.create_bottom_surface_pcd(bottom_surface_points)

        logging.info("Bottom surface completed successfully.")
        return pcd + bottom_surface_pcd, bottom_surface_pcd

    def compute_convex_hull(self, pcd):
        """Compute the convex hull of the point cloud."""
        logging.info("Computing convex hull.")
        hull, _ = pcd.compute_convex_hull()
        logging.info("Convex hull computed successfully.")
        return hull

    def sample_hull_surface(self, hull, num_samples=15000):
        """Sample points from the convex hull surface."""
        logging.info("Sampling points from the convex hull surface.")
        sample_points = hull.sample_points_uniformly(number_of_points=num_samples)
        outer_shape_pcd = o3d.geometry.PointCloud()
        outer_shape_pcd.points = sample_points.points
        logging.info("Points sampled successfully.")
        return outer_shape_pcd

    def extract_bottom_surface(self, outer_shape_pcd, depth):
        """Estimate normals and extract bottom surface points using RANSAC."""
        logging.info("Finding planes using RANSAC.")
        plane_model, inliers = outer_shape_pcd.segment_plane(distance_threshold=depth, ransac_n=3, num_iterations=1000)
        logging.info("Bottom surface points extracted.")
        return outer_shape_pcd.select_by_index(inliers)

    def create_bottom_surface_pcd(self, bottom_surface_points):
        """Create a point cloud for the bottom surface."""
        bottom_surface_pcd = o3d.geometry.PointCloud()
        bottom_surface_pcd.points = bottom_surface_points.points

        if self.main_object.has_colors():
            avg_color = np.mean(np.asarray(self.main_object.colors), axis=0)
            bottom_surface_pcd.paint_uniform_color(avg_color)

        return bottom_surface_pcd

    def calculate_bson_size(self, points, colors):
        """
        Estimate BSON document size for points and colors arrays.

        Args:
            points: numpy array of points
            colors: numpy array of colors

        Returns:
            int: Estimated size in bytes
        """
        # Estimate size of points array (each point has 3 float64 values)
        points_size = len(points) * 3 * 8  # 8 bytes per float64

        # Estimate size of colors array (each color has 3 uint8 values)
        colors_size = len(colors) * 3

        # Add overhead for BSON structure (approximate)
        overhead = 1000  # Base document overhead

        return (points_size + colors_size + overhead)*5

    def save_to_db(self, name='point_cloud', max_size_bytes=16 * 1024 * 1024):
        """
        Save the main object from the PLY file into MongoDB with automatic downsampling if needed.

        Args:
            name: Name for the point cloud
            max_size_bytes: Maximum allowed BSON document size (default: 16MB)

        Returns:
            str: ID of saved point cloud
        """
        if self.main_object is None:
            raise ValueError("Main object not processed yet. Run `remove_background()` first.")

        # Convert point cloud to numpy arrays
        points = np.asarray(self.main_object.points)
        colors = np.asarray(self.main_object.colors)

        if len(colors) == 0:
            logging.warning("No colors found in the main object. Defaulting to black color.")
            colors = np.zeros((len(points), 3))
            colors[:, 1] = 1  # Set green channel to 1

        # Scale color values from [0, 1] to [0, 255]
        colors = (colors * 255).astype(np.uint8)

        # Initial size check
        current_size = self.calculate_bson_size(points, colors)
        print(f"point cloud size: {current_size / (1024 * 1024):.2f} MB")

        # If size is too large, progressively downsample until it fits
        current_pcd = self.main_object
        voxel_size = 0.002  # Start with small voxel size

        while current_size > max_size_bytes:


            # Downsample with current voxel size
            current_pcd = self.voxel_downsample(current_pcd, voxel_size)

            # Update arrays
            points = np.asarray(current_pcd.points)
            colors = np.asarray(current_pcd.colors)
            if len(colors) == 0:
                colors = np.zeros((len(points), 3))
                colors[:, 1] = 1

            colors = (colors * 255).astype(np.uint8)

            # Recalculate size
            current_size = self.calculate_bson_size(points, colors)

            # Increase voxel size for next iteration if needed
            voxel_size *= 1.5

        # Convert the points and colors to the correct format
        formatted_points = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in points])
        formatted_colors = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in colors])

        # Save PointCloud
        point_cloud = PointCloud(name, formatted_points, formatted_colors)
        point_cloud_id = point_cloud.save()

        print(
            f"Successfully saved {len(formatted_points)} points to database with ID {point_cloud_id}. "
            f"Final size: {current_size / (1024 * 1024):.2f} MB"
        )

        return point_cloud_id



    def save_ply_file_system(self, main_object, title, id=None, max_size_mb=12):
        """
        Save a PLY file to the file system with automatic downsampling if the file size exceeds the limit.

        Args:
            main_object (open3d.geometry.PointCloud): The 3D object to be saved as PLY.
            title (str): The title of the PLY file.
            id (str): The identifier for the folder where the PLY file will be saved.
            max_size_mb (float): Maximum allowed file size in megabytes (default: 12MB)

        Returns:
            str: The full path of the saved PLY file.
        """
        if id is None:
            raise ValueError("An ID must be provided to save the PLY file.")

        if not isinstance(main_object, o3d.geometry.PointCloud):
            raise TypeError("main_object must be an Open3D PointCloud")

        # Define the base directory and create it if it doesn't exist
        base_dir = "/app/app/ply_preprocess_visuals"
        os.makedirs(base_dir, exist_ok=True)

        # Create the directory for this specific ID
        ply_dir = os.path.join(base_dir, title)
        os.makedirs(ply_dir, exist_ok=True)

        # Create the full file path
        file_name = f"{str(id)}.ply"
        file_path = os.path.join(ply_dir, file_name)

        def get_file_size_mb(filepath):
            """Get file size in megabytes"""
            return os.path.getsize(filepath) / (1024 * 1024)

        def save_and_check_size(pcd, filepath):
            """Save point cloud and return file size in MB"""
            success = o3d.io.write_point_cloud(filepath, pcd)
            if not success:
                raise IOError("Failed to write point cloud")
            return get_file_size_mb(filepath)

        def copy_point_cloud(pcd):
            """Create a deep copy of an Open3D point cloud"""
            new_pcd = o3d.geometry.PointCloud()
            new_pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points))
            if hasattr(pcd, 'colors') and pcd.colors:
                new_pcd.colors = o3d.utility.Vector3dVector(np.asarray(pcd.colors))
            if hasattr(pcd, 'normals') and pcd.normals:
                new_pcd.normals = o3d.utility.Vector3dVector(np.asarray(pcd.normals))
            return new_pcd

        try:
            # Initial save attempt
            current_pcd = copy_point_cloud(main_object)
            current_size = save_and_check_size(current_pcd, file_path)
            initial_points = len(current_pcd.points)

            logging.info(f"Initial PLY file size: {current_size:.2f}MB with {initial_points} points")

            # If size is too large, progressively downsample until it fits
            voxel_size = 0.002  # Start with small voxel size
            while current_size > max_size_mb:

                # Remove existing oversized file
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Downsample with current voxel size
                current_pcd = current_pcd.voxel_down_sample(voxel_size)

                # Save and check new size
                current_size = save_and_check_size(current_pcd, file_path)

                # Increase voxel size for next iteration if needed
                voxel_size *= 1.5

            # Calculate reduction statistics
            final_points = len(current_pcd.points)
            reduction_percent = ((initial_points - final_points) / initial_points) * 100 if initial_points > 0 else 0

            logging.info(
                f"PLY file saved successfully at: {file_path}\n"
                f"Final size: {current_size:.2f}MB\n"
                f"Points reduced: {initial_points:,} → {final_points:,} "
                f"({reduction_percent:.1f}% reduction)"
            )

            # Return filepath only if save was successful
            return file_path

        except Exception as e:
            logging.error(f"Error saving PLY file: {str(e)}")
            # Clean up any partially written file
            if os.path.exists(file_path):
                os.remove(file_path)
            return None







    def numpy_to_python(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    def format_point_cloud_to_serializable(self, ply):
        if ply is None:
            raise ValueError("Main object not processed yet. Run `remove_background()` first.")

        # Convert point cloud to numpy arrays
        points = np.asarray(ply.points)  # Shape (N, 3)
        colors = np.asarray(ply.colors)  # Shape (N, 3)

        if len(colors) == 0:
            logging.warning("No colors found in the main object. Defaulting to black color.")
            colors = np.zeros((len(points), 3))  # Initialize with zeros
            colors[:, 1] = 1  # Set green channel to 1 for green color

        # Scale color values from [0, 1] to [0, 255]
        colors = (colors * 255).astype(np.uint8)

        # Convert the points_3d array to a list of dictionaries
        formatted_points = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in points])
        formatted_colors = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in colors])

        # Save PointCloud
        point_cloud = PointCloud("format", formatted_points, formatted_colors)
        return {
            'type': 'scatter3d',
            'mode': 'markers',
            'x': self.numpy_to_python(point_cloud.points[:, 0]),
            'y': self.numpy_to_python(point_cloud.points[:, 1]),
            'z': self.numpy_to_python(point_cloud.points[:, 2]),
            'marker': {
                'size': 1.5,
                'color': self.numpy_to_python(
                    point_cloud.colors) if point_cloud.colors is not None else 'rgb(100, 100, 100)',
                'opacity': 1
            }
        }

    def get_ply(self, param):
        try:
            pcd = o3d.io.read_point_cloud("/app/app/ply_preprocess_visuals/"+param+"/" + self.ply_id + ".ply")
            if not pcd.has_points():
                pcd = None
            return pcd
        except:
            logging.error("error in load original ply: " + self.ply_id)
            return None
