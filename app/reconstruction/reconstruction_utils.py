import numpy as np
import pandas as pd
import logging
from flask import current_app


logger = logging.getLogger(__name__)

def load_point_cloud_from_csv(filename):
    """
    Load point cloud data from a CSV file.

    Args:
        filename (str): Path to the CSV file containing point cloud data.

    Returns:
        tuple: (points, colors) where points is a numpy array of 3D coordinates
               and colors is a numpy array of RGB values (or None if not present).
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)

        # Check if the file has a header
        if not all(col in df.columns for col in ['x', 'y', 'z']):
            df = pd.read_csv(filename, header=None)
            df.columns = ['x', 'y', 'z'] + [f'col_{i}' for i in range(3, len(df.columns))]

        # Extract points
        points = df[['x', 'y', 'z']].values

        # Extract colors if present
        if all(col in df.columns for col in ['r', 'g', 'b']):
            colors = df[['r', 'g', 'b']].values
        elif len(df.columns) > 3:
            colors = df.iloc[:, 3:6].values
        else:
            colors = None

        logger.info(f"Loaded {len(points)} points from {filename}")
        return points, colors
    except Exception as e:
        logger.error(f"Error loading point cloud from CSV: {str(e)}")
        raise

def generate_colors(points, method='height'):
    """
    Generate colors for points if original data doesn't include color information.

    Args:
        points (list or numpy.ndarray): List or array of 3D point coordinates.
        method (str): Method to generate colors. Options: 'random', 'height', 'distance'

    Returns:
        numpy.ndarray: Array of RGB color values for each point.
    """
    # Convert points to numpy array if it's a list
    points = np.array(points) if isinstance(points, list) else points

    if method == 'random':
        return np.random.rand(len(points), 3)
    elif method == 'height':
        # Color based on height (z-coordinate)
        z_values = points[:, 2]
        colors = np.zeros((len(points), 3))
        z_min, z_max = z_values.min(), z_values.max()
        if z_min != z_max:  # Avoid division by zero
            colors[:, 0] = (z_values - z_min) / (z_max - z_min)  # Red channel
        else:
            colors[:, 0] = 0.5  # Set to middle value if all points have the same height
        colors[:, 2] = 1 - colors[:, 0]  # Blue channel
        return colors
    elif method == 'distance':
        # Color based on distance from center
        center = np.mean(points, axis=0)
        distances = np.linalg.norm(points - center, axis=1)
        colors = np.zeros((len(points), 3))
        d_min, d_max = distances.min(), distances.max()
        if d_min != d_max:  # Avoid division by zero
            colors[:, 0] = (distances - d_min) / (d_max - d_min)  # Red channel
        else:
            colors[:, 0] = 0.5  # Set to middle value if all points are equidistant
        colors[:, 2] = 1 - colors[:, 0]  # Blue channel
        return colors
    else:
        raise ValueError(f"Unknown color generation method: {method}")

