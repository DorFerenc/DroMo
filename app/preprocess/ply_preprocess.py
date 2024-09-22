import open3d as o3d
import numpy as np
import csv
from app.db.mongodb import get_db
from bson import ObjectId

from app.models.point_cloud import PointCloud


class PLYProcessor:
    """Handles operations related to processing and saving PLY files."""

    def __init__(self, ply_file):
        self.ply_file = ply_file
        self.main_object = None

    def preprocess(self, distance_threshold=0.02, ransac_n=8, num_iterations=1000, cluster_eps=0.05,
                          min_points=50):
        """
        Remove the background from a point cloud file and extract the main object.
        """
        # Load the point cloud
        pcd = o3d.io.read_point_cloud(self.ply_file)

        # Apply RANSAC to segment the plane
        plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                                 ransac_n=ransac_n,
                                                 num_iterations=num_iterations)

        # Select the outlier points (which do not belong to the plane)
        remaining_cloud = pcd.select_by_index(inliers, invert=True)

        # Perform DBSCAN clustering on the remaining points
        labels = np.array(remaining_cloud.cluster_dbscan(eps=cluster_eps, min_points=min_points))

        if len(labels) == 0:
            print("Clustering failed. Returning all non-plane points.")
            self.main_object = remaining_cloud
            return self.main_object

        # Find the largest cluster (assumed to be the main object)
        max_label = labels.max()
        cluster_sizes = [len(labels[labels == i]) for i in range(max_label + 1)]
        if len(cluster_sizes) == 0 or max_label == -1:
            print("No clusters found. Returning all non-plane points.")
            self.main_object = remaining_cloud
            return self.main_object
        largest_cluster = np.argmax(cluster_sizes)

        # Extract the largest cluster
        self.main_object = remaining_cloud.select_by_index(np.where(labels == largest_cluster)[0])

        return self.main_object

    def save_to_db(self, name='point_cloud'):
        """
        Save the main object from the PLY file into MongoDB and write it to a CSV file.
        """
        if self.main_object is None:
            raise ValueError("Main object not processed yet. Run `remove_background()` first.")

        # Convert point cloud to numpy arrays
        points = np.asarray(self.main_object.points)  # Shape (N, 3)
        colors = np.asarray(self.main_object.colors)  # Shape (N, 3)

        # Scale color values from [0, 1] to [0, 255]
        colors = (colors * 255).astype(np.uint8)

        # Combine points and colors
        combined_array = np.hstack((points, colors))

        # Prepare the point data for MongoDB
        # formatted_points = [{'x': float(p[0]), 'y': float(p[1]), 'z': float(p[2]), 'r': int(p[3]), 'g': int(p[4]), 'b': int(p[5])}
        #                     for p in combined_array]
        # Convert the points_3d array to a list of dictionaries
        formatted_points = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in combined_array])
        formatted_colors = np.array([[float(p[3]), float(p[4]), float(p[5])] for p in combined_array])

        # Save PointCloud
        point_cloud = PointCloud(name, formatted_points, formatted_colors)
        # # Write the point cloud data to a CSV file
        # with open('app/points/3d_points.csv', 'w') as f:
        #     f.write(point_cloud.to_string())
        # Insert into MongoDB
        point_cloud_id = point_cloud.save()
        print(f"3D reconstruction complete. {len(formatted_points)} points saved to the database with ID {point_cloud_id}.")
        return point_cloud_id
