import logging

import open3d as o3d
import numpy as np


from app.models.point_cloud import PointCloud


class PLYProcessor:
    """Handles operations related to processing and saving PLY files."""

    def __init__(self, ply_file):
        self.ply_file = ply_file
        self.main_object = None

    def preprocess(self, distance_threshold=0.01, ransac_n=3, num_iterations=1000, cluster_eps=0.02,
                          min_points=50):
        """
        Remove the background from a point cloud file and extract the main object.
        """
        pcd = self.load_point_cloud()
        # Center the point cloud
        center_pcd = self.center_point_cloud(pcd)
        # Remove statistical outliers
        filtered_pcd = self.remove_statistical_outliers(center_pcd)
        # Voxel downsampling
        filtered_pcd = self.voxel_downsample(filtered_pcd)
        # Estimate normals
        filtered_pcd = self.estimate_normals(filtered_pcd)
        #
        self.segment_plane(filtered_pcd, distance_threshold, ransac_n, num_iterations)
        remaining_cloud = self.get_remaining_cloud(pcd)
        #
        self.cluster_points(remaining_cloud, cluster_eps, min_points)
        #
        self.main_object = self.complete_bottom(self.main_object)

        self.main_object = self.center_point_cloud(self.main_object)

        return self.main_object


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

    def estimate_normals(self, pcd):
        """
        Estimate normals for the point cloud.
        :param pcd: Input point cloud.
        :return: Point cloud with estimated normals.
        """
        nn_distance = np.mean(pcd.compute_nearest_neighbor_distance())
        radius_normals = nn_distance * 10
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normals, max_nn=30),
            fast_normal_computation=True
        )
        logging.info("Normals estimated for the point cloud.")

        return pcd
    def segment_plane(self, pcd, distance_threshold, ransac_n, num_iterations):
        """Segment the largest plane from the point cloud."""
        logging.info("Segmenting the largest plane from the point cloud.")
        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                 ransac_n=ransac_n,
                                                 num_iterations=num_iterations)
        logging.info("Plane segmentation completed.")
        self.main_object = pcd.select_by_index(inliers, invert=True)  # Store non-plane points

    def get_remaining_cloud(self, pcd):
        """Return the remaining cloud (non-plane points) after plane segmentation."""
        logging.info("Extracting remaining points from the point cloud.")
        return self.main_object

    def cluster_points(self, remaining_cloud, cluster_eps, min_points):
        """Cluster remaining points to find the main object."""
        logging.info("Clustering remaining points.")
        labels = np.array(remaining_cloud.cluster_dbscan(eps=cluster_eps, min_points=min_points))

        if len(labels) == 0:
            logging.warning("Clustering failed. Returning all non-plane points.")
            self.main_object = remaining_cloud
            return

        # Find the largest cluster (assumed to be the main object)
        max_label = labels.max()
        logging.info(f"Point cloud has {max_label + 1} clusters")
        cluster_sizes = [len(labels[labels == i]) for i in range(max_label + 1)]
        largest_cluster = np.argmax(cluster_sizes)

        # Extract the largest cluster
        self.main_object = remaining_cloud.select_by_index(np.where(labels == largest_cluster)[0])
        logging.info("Largest cluster extracted successfully.")

    def complete_bottom(self, pcd, resolution=0.005, depth=0.005):
        """Complete the bottom of the object."""
        logging.info("Completing the bottom of the object.")
        hull = self.compute_convex_hull(pcd)
        outer_shape_pcd = self.sample_hull_surface(hull)

        bottom_surface_points = self.extract_bottom_surface(outer_shape_pcd, depth)
        bottom_surface_pcd = self.create_bottom_surface_pcd(bottom_surface_points)
        logging.info("Bottom surface completed successfully.")
        return pcd + bottom_surface_pcd

    def compute_convex_hull(self, pcd):
        """Compute the convex hull of the point cloud."""
        logging.info("Computing convex hull.")
        hull, _ = pcd.compute_convex_hull()
        logging.info("Convex hull computed successfully.")
        return hull

    def sample_hull_surface(self, hull, num_samples=4000):
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

    def save_to_db(self, name='point_cloud'):
        """
        Save the main object from the PLY file into MongoDB and write it to a CSV file.
        """
        if self.main_object is None:
            raise ValueError("Main object not processed yet. Run `remove_background()` first.")

        # Convert point cloud to numpy arrays
        points = np.asarray(self.main_object.points)  # Shape (N, 3)
        colors = np.asarray(self.main_object.colors)  # Shape (N, 3)

        if len(colors) == 0:
            logging.warning("No colors found in the main object. Defaulting to black color.")
            colors = np.zeros((len(points), 3))  # Initialize with zeros
            colors[:, 1] = 1  # Set green channel to 1 for green color

        # Scale color values from [0, 1] to [0, 255]
        colors = (colors * 255).astype(np.uint8)

        # Convert the points_3d array to a list of dictionaries
        formatted_points = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in points])
        formatted_colors = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in colors])
        print(f"3D reconstruction complete. {len(formatted_points)}  {len(formatted_colors)}")

        # Save PointCloud
        point_cloud = PointCloud(name, formatted_points, formatted_colors)
        point_cloud_id = point_cloud.save()
        print(f"3D reconstruction complete. {len(formatted_points)} points saved to the database with ID {point_cloud_id}.")
        return point_cloud_id
