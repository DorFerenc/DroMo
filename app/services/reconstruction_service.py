# reconstruction_service.py
import pandas as pd
import os
from typing import Tuple, Optional
import numpy as np
import pyvista as pv
pv.OFF_SCREEN = True  # Disable the need for graphical output
from reconstruction.point_cloud_to_mesh import PointCloudToMesh
from reconstruction.texture_mapper import TextureMapper
from reconstruction.mesh_to_obj_converter import MeshToOBJConverter
import logging
from typing import Tuple, Optional

class ReconstructionService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pc_to_mesh = PointCloudToMesh()
        self.texture_mapper = TextureMapper()
        self.mesh_to_obj_converter = MeshToOBJConverter()
        self.mesh_to_obj = None

    # def reconstruct(self, point_cloud_data: np.ndarray, colors: Optional[np.ndarray] = None) -> Tuple[pv.PolyData, str, str]:
    #     """
    #     Perform the entire reconstruction process.

    #     Args:
    #         point_cloud_data (np.ndarray): Array of 3D point coordinates.
    #         colors (np.ndarray, optional): Array of RGB color values for each point.

    #     Returns:
    #         Tuple[pv.PolyData, str, str]: Textured mesh, OBJ filename, and texture filename.

    #     Raises:
    #         ValueError: If the input data is invalid.
    #     """
    #     self.logger.info("Starting reconstruction process")

    #     try:
    #         # Generate mesh
    #         mesh = self.generate_mesh(point_cloud_data)

    #         # Refine mesh
    #         refined_mesh = self.refine_mesh(mesh)

    #         # Apply texture
    #         if colors is None:
    #             colors = self.generate_colors(point_cloud_data)
    #         textured_mesh = self.apply_texture(refined_mesh, point_cloud_data, colors)

    #         # Save as OBJ
    #         obj_filename, texture_filename = self.save_as_obj(textured_mesh)

    #         self.logger.info("Reconstruction process completed successfully")
    #         return textured_mesh, obj_filename, texture_filename

    #     except Exception as e:
    #         self.logger.error(f"Error in reconstruction process: {str(e)}")
    #         raise

    # def generate_mesh(self, point_cloud: np.ndarray) -> pv.PolyData:
    #     self.logger.info("Generating mesh")
    #     self.pc_to_mesh.set_point_cloud(point_cloud)
    #     return self.pc_to_mesh.generate_mesh()

    # def refine_mesh(self, mesh: pv.PolyData) -> pv.PolyData:
    #     self.logger.info("Refining mesh")
    #     return self.mesh_refiner.refine_mesh(mesh)

    # def apply_texture(self, mesh: pv.PolyData, point_cloud: np.ndarray, colors: np.ndarray) -> pv.PolyData:
    #     self.logger.info("Applying texture")
    #     self.texture_mapper.load_mesh(mesh)
    #     self.texture_mapper.load_point_cloud_with_colors(point_cloud, colors)
    #     self.texture_mapper.apply_texture()
    #     return self.texture_mapper.get_textured_mesh()

    # def save_as_obj(self, textured_mesh: pv.PolyData) -> Tuple[str, str]:
    #     self.logger.info("Saving as OBJ")
    #     obj_filename = "output_mesh.obj"
    #     texture_filename = "output_texture.png"
    #     self.mesh_to_obj = MeshToOBJConverter(textured_mesh, self.texture_mapper)
    #     self.mesh_to_obj.convert_and_save(obj_filename, texture_filename)
    #     return obj_filename, texture_filename

    # @staticmethod
    # def generate_colors(points: np.ndarray, method: str = 'height') -> np.ndarray:
    #     if method == 'random':
    #         return np.random.rand(len(points), 3)
    #     elif method == 'height':
    #         z_values = points[:, 2]
    #         colors = np.zeros((len(points), 3))
    #         colors[:, 0] = (z_values - z_values.min()) / (z_values.max() - z_values.min())
    #         colors[:, 2] = 1 - colors[:, 0]
    #         return colors
    #     elif method == 'distance':
    #         center = np.mean(points, axis=0)
    #         distances = np.linalg.norm(points - center, axis=1)
    #         colors = np.zeros((len(points), 3))
    #         colors[:, 0] = (distances - distances.min()) / (distances.max() - distances.min())
    #         colors[:, 2] = 1 - colors[:, 0]
    #         return colors
    #     else:
    #         raise ValueError(f"Unknown color generation method: {method}")

    # @staticmethod
    # def load_point_cloud_from_csv(filename: str) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    #     try:
    #         df = pd.read_csv(filename)
    #         if not all(col in df.columns for col in ['x', 'y', 'z']):
    #             df = pd.read_csv(filename, header=None)
    #             df.columns = ['x', 'y', 'z'] + [f'col_{i}' for i in range(3, len(df.columns))]

    #         points = df[['x', 'y', 'z']].values
    #         colors = df[['r', 'g', 'b']].values if all(col in df.columns for col in ['r', 'g', 'b']) else None

    #         return points, colors
    #     except Exception as e:
    #         raise ValueError(f"Error loading point cloud from CSV: {str(e)}")