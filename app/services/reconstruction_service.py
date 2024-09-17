import os
from bson import ObjectId
from flask import current_app
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
                ReconstructionService.logger.info("Generating colors for point cloud")
                colors = generate_colors(points, method='height')

            # Convert point cloud to mesh
            ReconstructionService.logger.info("Converting point cloud to mesh")
            pc_to_mesh = PointCloudToMesh()
            try:
                pc_to_mesh.set_point_cloud(points)
                mesh = pc_to_mesh.generate_mesh()
            except ValueError as e:
                ReconstructionService.logger.error(f"Error generating mesh: {str(e)}")
                raise ValueError(f"Failed to generate mesh: {str(e)}")

            # Apply textures
            ReconstructionService.logger.info("Applying textures to mesh")
            texture_mapper = TextureMapper()
            try:
                texture_mapper.load_mesh(mesh)
                texture_mapper.load_point_cloud_with_colors(points, colors)
                texture_mapper.apply_texture()
            except Exception as e:
                ReconstructionService.logger.error(f"Error applying texture: {str(e)}")
                raise ValueError(f"Failed to apply texture: {str(e)}")

            # Create a unique folder for this model, including the point cloud name
            point_cloud_name = point_cloud.get('name')
            # Generate colors if not present
            if point_cloud_name is None:
                ReconstructionService.logger.error(f"Point cloud name: {point_cloud_id} not found")
                raise ValueError("Point cloud name not found")
            safe_name = ''.join(c if c.isalnum() else '_' for c in point_cloud_name)  # Sanitize the name
            model_name = f"{safe_name}_{point_cloud_id}"
            # output_dir = os.path.join('/app/outputs', model_name)
            output_dir = os.path.join(current_app.config['MODELS_FOLDER'], model_name)
            os.makedirs(output_dir, exist_ok=True)

            if not os.access(output_dir, os.W_OK):
                ReconstructionService.logger.error(f"No write permission for directory: {output_dir}")
                raise PermissionError(f"No write permission for directory: {output_dir}")

            # Define filenames
            obj_filename = os.path.join(output_dir, f"{model_name}.obj")
            mtl_filename = os.path.join(output_dir, f"{model_name}.mtl")
            texture_filename = os.path.join(output_dir, f"{model_name}.png")

            # Convert to OBJ and save files
            ReconstructionService.logger.info(f"Converting mesh to OBJ and saving files to {output_dir}")
            textured_mesh = texture_mapper.get_textured_mesh()
            obj_converter = MeshToOBJConverter(textured_mesh, texture_mapper)
            try:
                obj_converter.convert_and_save(obj_filename, texture_filename)
                ReconstructionService.logger.info(f"OBJ file saved as {obj_filename}")
                ReconstructionService.logger.info(f"Texture file saved as {texture_filename}")
            except Exception as e:
                ReconstructionService.logger.error(f"Error saving OBJ and texture files: {str(e)}")
                raise ValueError(f"Failed to save OBJ and texture files: {str(e)}")

            # Verify that files were actually created
            for filename in [obj_filename, mtl_filename, texture_filename]:
                if not os.path.exists(filename):
                    ReconstructionService.logger.error(f"File not created: {filename}")
                    raise FileNotFoundError(f"File not created: {filename}")

            # Create and save model metadata
            ReconstructionService.logger.info("Saving model metadata to database")
            model = ThreeDModel(
                name=model_name,
                folder_path=output_dir,
                point_cloud_id=point_cloud_id,
                obj_file=obj_filename,
                mtl_file=mtl_filename, # this is null currently
                texture_file=texture_filename
            )
            model_id = model.save()

            ReconstructionService.logger.info(f"Reconstruction completed successfully. Model ID: {model_id}")
            return str(model_id)

        except Exception as e:
            ReconstructionService.logger.error(f"Reconstruction error: {str(e)}", exc_info=True)
            raise