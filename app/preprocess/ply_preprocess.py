import open3d as o3d
import numpy as np
import logging
import os

class PLYProcessor:
    """
    Class to process a PLY file, remove background, and extract the main object.
    """

    def __init__(self, distance_threshold=0.01, ransac_n=8, num_iterations=1000, cluster_eps=0.05, min_points=100):
        """
        Initialize the PLYProcessor with default or custom parameters.

        Args:
            distance_threshold (float): Threshold for RANSAC plane segmentation.
            ransac_n (int): Number of points to sample for RANSAC.
            num_iterations (int): Number of iterations for RANSAC.
            cluster_eps (float): Maximum distance for DBSCAN clustering.
            min_points (int): Minimum points to form a cluster.
        """
        self.distance_threshold = distance_threshold
        self.ransac_n = ransac_n
        self.num_iterations = num_iterations
        self.cluster_eps = cluster_eps
        self.min_points = min_points

    def process(self, ply_file, output_dir):
        """
        Process a PLY file, remove the background, and extract the main object.

        Args:
            ply_file (str): Path to the PLY file.
            output_dir (str): Directory to save the processed file.

        Returns:
            int: Number of points in the extracted main object.
        """
        try:
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Load the point cloud
            pcd = o3d.io.read_point_cloud(ply_file)
            logging.info(f"Loaded point cloud from {ply_file}, containing {len(pcd.points)} points.")

            # Apply RANSAC to segment the plane
            plane_model, inliers = pcd.segment_plane(distance_threshold=self.distance_threshold,
                                                     ransac_n=self.ransac_n,
                                                     num_iterations=self.num_iterations)
            logging.info(f"Plane detected with RANSAC, {len(inliers)} points considered part of the plane (background).")

            # Select the outlier points (not part of the plane)
            remaining_cloud = pcd.select_by_index(inliers, invert=True)
            logging.info(f"Remaining point cloud contains {len(remaining_cloud.points)} points.")

            # Perform DBSCAN clustering on the remaining points
            labels = np.array(remaining_cloud.cluster_dbscan(eps=self.cluster_eps, min_points=self.min_points))

            if len(labels) == 0:
                logging.warning("Clustering failed. Returning all non-plane points.")
                main_object = remaining_cloud
            else:
                # Find the largest cluster
                max_label = labels.max()
                logging.info(f"Point cloud has {max_label + 1} clusters.")

                cluster_sizes = [len(labels[labels == i]) for i in range(max_label + 1)]
                largest_cluster = np.argmax(cluster_sizes)

                # Extract the largest cluster
                main_object = remaining_cloud.select_by_index(np.where(labels == largest_cluster)[0])
                logging.info(f"Extracted the largest cluster with {len(main_object.points)} points.")

            # Save the processed point cloud (main object)
            output_file = os.path.join(output_dir, "main_object.ply")
            o3d.io.write_point_cloud(output_file, main_object)
            logging.info(f"Processed point cloud saved to {output_file}.")

            # Return the number of points in the main object for tracking
            return len(main_object.points)

        except Exception as e:
            logging.error(f"Error processing PLY file {ply_file}: {e}")
            return -1
