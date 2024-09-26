# File: app/services/threed_visualization.py

import numpy as np
import pyvista as pv
from PIL import Image
from flask import current_app
from app.models.threed_model import ThreeDModel
from app.models.point_cloud import PointCloud

class ReconProcVisualizationService:
    @staticmethod
    def get_point_cloud_data(model_id):
        model = ThreeDModel.get_by_id(model_id)
        if not model:
            current_app.logger.error(f"Model not found: {model_id}")
            return None

        point_cloud = PointCloud.get_by_id(model.point_cloud_id)
        if not point_cloud:
            current_app.logger.error(f"Point cloud not found for model: {model_id}")
            return None

        return {
            'type': 'scatter3d',
            'mode': 'markers',
            'x': point_cloud.points[:, 0].tolist(),
            'y': point_cloud.points[:, 1].tolist(),
            'z': point_cloud.points[:, 2].tolist(),
            'marker': {
                'size': 1.5,
                'color': point_cloud.colors.tolist() if point_cloud.colors is not None else 'rgb(100, 100, 100)',
                'opacity': 1
            }
        }

    @staticmethod
    def get_mesh_data(model_id, mesh_type='initial'):
        model = ThreeDModel.get_by_id(model_id)
        if not model:
            current_app.logger.error(f"Model not found: {model_id}")
            return None

        current_app.logger.info(f"Loading OBJ file: {model.obj_file}")
        mesh = pv.read(model.obj_file)
        mesh_data = ThreeDVisualizationService.extract_mesh_data(mesh)

        if mesh_type == 'initial':
            color = 'rgb(255, 165, 0)'
        elif mesh_type == 'refined':
            color = 'rgb(255, 140, 0)'
        else:
            color = 'rgb(100, 100, 100)'

        return ThreeDVisualizationService.create_mesh_data(mesh_data, surface_color=color, wireframe_color='rgb(0, 0, 0)')

    @staticmethod
    def get_textured_mesh_data(model_id):
        model = ThreeDModel.get_by_id(model_id)
        if not model:
            current_app.logger.error(f"Model not found: {model_id}")
            return None

        current_app.logger.info(f"Loading OBJ file: {model.obj_file}")
        mesh = pv.read(model.obj_file)
        mesh_data = ThreeDVisualizationService.extract_mesh_data(mesh)

        current_app.logger.info(f"Processing texture: {model.texture_file}")
        try:
            texture = Image.open(model.texture_file)
            texture_array = np.array(texture)

            current_app.logger.info("Mapping texture to vertices")
            if mesh.active_t_coords is not None:
                u = np.clip(mesh.active_t_coords[:, 0], 0, 1)
                v = np.clip(mesh.active_t_coords[:, 1], 0, 1)
                x = np.floor(u * (texture_array.shape[1] - 1)).astype(int)
                y = np.floor((1 - v) * (texture_array.shape[0] - 1)).astype(int)
                vertex_colors = texture_array[y, x]
            else:
                current_app.logger.warning("No texture coordinates found, using default color")
                vertex_colors = np.full((len(mesh.points), 3), [200, 200, 200])

            mesh_data['point_data']['RGB'] = vertex_colors

        except Exception as e:
            current_app.logger.error(f"Error processing texture: {str(e)}")
            mesh_data['point_data']['RGB'] = np.full((len(mesh_data['points']), 3), [200, 200, 200])

        return [{
            'type': 'mesh3d',
            'x': mesh_data['points'][:, 0].tolist(),
            'y': mesh_data['points'][:, 1].tolist(),
            'z': mesh_data['points'][:, 2].tolist(),
            'i': mesh_data['faces'][:, 0].tolist(),
            'j': mesh_data['faces'][:, 1].tolist(),
            'k': mesh_data['faces'][:, 2].tolist(),
            'vertexcolor': mesh_data['point_data']['RGB'].tolist(),
            'flatshading': False,
            'lighting': {
                'ambient': 0.8,
                'diffuse': 1,
                'fresnel': 1,
                'specular': 2,
                'roughness': 0.05,
            },
            'lightposition': {'x': 100, 'y': 200, 'z': 150},
            'opacity': 1.0
        }]

    @staticmethod
    def extract_mesh_data(mesh):
        current_app.logger.info("Extracting mesh data")
        return {
            'points': mesh.points,
            'faces': mesh.faces.reshape(-1, 4)[:, 1:],  # Convert to [i, j, k] format
            'point_data': {key: mesh.point_data[key] for key in mesh.point_data.keys()}
        }

    @staticmethod
    def create_mesh_data(mesh_data, surface_color='rgb(255, 165, 0)', wireframe_color='rgb(0, 0, 0)'):
        current_app.logger.info("Creating mesh data")
        surface = {
            'type': 'mesh3d',
            'x': mesh_data['points'][:, 0].tolist(),
            'y': mesh_data['points'][:, 1].tolist(),
            'z': mesh_data['points'][:, 2].tolist(),
            'i': mesh_data['faces'][:, 0].tolist(),
            'j': mesh_data['faces'][:, 1].tolist(),
            'k': mesh_data['faces'][:, 2].tolist(),
            'color': surface_color,
            'flatshading': True,
            'lighting': {
                'ambient': 0.8,
                'diffuse': 0.9,
                'fresnel': 0.5,
                'specular': 0.5,
                'roughness': 0.5,
            },
            'lightposition': {'x': 100, 'y': 200, 'z': 150},
            'opacity': 1.0
        }

        wireframe = {
            'type': 'scatter3d',
            'mode': 'lines',
            'x': [],
            'y': [],
            'z': [],
            'line': {
                'color': wireframe_color,
                'width': 1
            },
            'opacity': 1.0
        }

        for face in mesh_data['faces']:
            for i in range(3):
                p1, p2 = mesh_data['points'][face[i]], mesh_data['points'][face[(i + 1) % 3]]
                wireframe['x'].extend([p1[0], p2[0], None])
                wireframe['y'].extend([p1[1], p2[1], None])
                wireframe['z'].extend([p1[2], p2[2], None])

        return [surface, wireframe]