import os
from bson import ObjectId
from app.db.mongodb import get_db
from app.reconstruction.point_cloud_to_mesh import PointCloudToMesh
from app.reconstruction.texture_mapper import TextureMapper
from app.reconstruction.mesh_to_obj_converter import MeshToOBJConverter
from app.reconstruction.reconstruction_utils import generate_colors
from app.models.threed_model import ThreeDModel
import logging

class ReconstructionService:
    logger = logging.getLogger(__name__)

    @staticmethod
    def start_reconstruction(point_cloud_id):
        ReconstructionService.logger.info(f"Starting reconstruction for point cloud {point_cloud_id}")

        db = get_db()
        if db is None:
            ReconstructionService.logger.error("Database connection is None")
            raise ValueError("Database connection failed")

        try:
            ReconstructionService.logger.info(f"Starting reconstruction for point cloud {point_cloud_id}")
            if db is None:
                ReconstructionService.logger.error("Database connection is None")
                raise ValueError("Database connection failed")
            # Retrieve point cloud data
            point_cloud = db.point_clouds.find_one({'_id': ObjectId(point_cloud_id)})
            if not point_cloud:
                ReconstructionService.logger.error(f"Point cloud {point_cloud_id} not found")
                raise ValueError("Point cloud not found")

            # points = point_cloud['points']
            points = point_cloud.get('points')
            if not points:
                raise ValueError("Point cloud has no points data")

            colors = point_cloud.get('colors')
            # Generate colors if not present
            if colors is None:
                colors = generate_colors(points, method='random')

            # Convert point cloud to mesh
            pc_to_mesh = PointCloudToMesh()
            try:
                pc_to_mesh.set_point_cloud(points)
                mesh = pc_to_mesh.generate_mesh()
            except ValueError as e:
                ReconstructionService.logger.error(f"Error generating mesh: {str(e)}")
                raise ValueError(f"Failed to generate mesh: {str(e)}")

            # Apply textures
            texture_mapper = TextureMapper()
            try:
                texture_mapper.load_mesh(mesh)
                texture_mapper.load_point_cloud_with_colors(points, colors)
                texture_mapper.apply_texture()
            except Exception as e:
                ReconstructionService.logger.error(f"Error applying texture: {str(e)}")
                raise ValueError(f"Failed to apply texture: {str(e)}")

            # Convert to OBJ and save files
            output_dir = 'outputs/models'
            os.makedirs(output_dir, exist_ok=True)
            base_filename = f"{output_dir}/model_{point_cloud_id}"
            obj_filename = f"{base_filename}.obj"
            mtl_filename = f"{base_filename}.mtl"
            texture_filename = f"{base_filename}.png"

            textured_mesh = texture_mapper.get_textured_mesh()
            # obj_converter = MeshToOBJConverter(mesh, texture_mapper)
            obj_converter = MeshToOBJConverter(textured_mesh, texture_mapper)
            obj_converter.convert_and_save(obj_filename, texture_filename)

            # Create and save model metadata
            model = ThreeDModel(
                point_cloud_id=point_cloud_id,
                obj_file=obj_filename,
                mtl_file=mtl_filename, # this is null currently
                texture_file=texture_filename
            )
            model_id = model.save()

            return str(model_id)

        except Exception as e:
            ReconstructionService.logger.error(f"Reconstruction error: {str(e)}", exc_info=True)
            raise