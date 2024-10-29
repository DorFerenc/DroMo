import numpy as np
from PIL import Image
import os
import logging


class MeshToOBJConverter:
    """
    A class for converting textured meshes to OBJ format.

    This class provides functionality to convert a textured mesh to OBJ format,
    including generating the associated MTL file and texture image.

    Attributes:
        mesh (pyvista.PolyData): The textured mesh to be converted.
        texture_mapper (TextureMapper): The TextureMapper object used for texture generation.
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, mesh, texture_mapper):
        """
        Initialize the MeshToOBJConverter.

        Args:
            mesh (pyvista.PolyData): The textured mesh to be converted.
            texture_mapper (TextureMapper): The TextureMapper object used for texture generation.
        """
        self.mesh = mesh
        self.texture_mapper = texture_mapper
        self.logger = logging.getLogger(self.__class__.__name__)

    def save_texture_image(self, texture_filename):
        """
        Generate and save the texture image.

        This method uses the TextureMapper to generate a texture image and saves it
        to a file.

        Args:
            texture_filename (str): The name of the output texture image file.

        Raises:
            Exception: If there's an error during texture image generation or saving.
        """
        try:
            texture_image = self.texture_mapper.generate_texture_image()

            # Convert to 8-bit color
            texture_image_8bit = (texture_image * 255).astype(np.uint8)

            image = Image.fromarray(texture_image_8bit)
            image.save(texture_filename)
            self.logger.info(f"Texture image saved as {texture_filename}")
        except Exception as e:
            # self.logger.error(f"Error saving texture image: {str(e)}")
            self.logger.error(f"Error saving texture image: {str(e)}", exc_info=True)
            raise

    def create_mtl_file(self, obj_filename, texture_filename):
        """
        Create the Material Template Library (MTL) file with material properties based on mesh characteristics.
        """
        try:
            mtl_filename = obj_filename.rsplit('.', 1)[0] + '.mtl'

            # Calculate average color from texture if available
            if 'RGB' in self.mesh.point_data:
                avg_color = np.mean(self.mesh.point_data['RGB'], axis=0)
                ka = avg_color * 0.2  # Ambient color (20% of average)
                kd = avg_color        # Diffuse color (100% of average)
                ks = np.ones(3) * 0.1 # Slight specular highlight
            else:
                ka = np.array([0.2, 0.2, 0.2])
                kd = np.array([0.8, 0.8, 0.8])
                ks = np.array([0.1, 0.1, 0.1])

            with open(mtl_filename, 'w') as f:
                f.write("# MTL file\n")
                f.write("newmtl material0\n")
                f.write(f"Ka {ka[0]:.3f} {ka[1]:.3f} {ka[2]:.3f}\n")  # Ambient
                f.write(f"Kd {kd[0]:.3f} {kd[1]:.3f} {kd[2]:.3f}\n")  # Diffuse
                f.write(f"Ks {ks[0]:.3f} {ks[1]:.3f} {ks[2]:.3f}\n")  # Specular
                f.write("Ns 10.0\n")  # Specular exponent
                f.write("d 1.0\n")    # Opacity
                f.write("illum 2\n")  # Illumination model
                f.write(f"map_Kd {os.path.basename(texture_filename)}\n")

            self.logger.info(f"MTL file saved as {mtl_filename}")
        except Exception as e:
            self.logger.error(f"Error creating MTL file: {str(e)}", exc_info=True)
            raise

    def convert_to_obj(self, output_filename):
        """
        Convert the mesh to OBJ format with corrected texture coordinates.
        """
        if 'UV' not in self.mesh.point_data:
            raise ValueError("Mesh does not have texture coordinates. Apply UV mapping before converting to OBJ.")

        try:
            vertices = self.mesh.points
            faces = self.mesh.faces

            with open(output_filename, 'w') as f:
                f.write("# OBJ file\n")
                f.write(f"mtllib {os.path.basename(output_filename.rsplit('.', 1)[0] + '.mtl')}\n")

                # Write vertices
                for v in vertices:
                    f.write(f"v {v[0]} {v[1]} {v[2]}\n")

                # Write texture coordinates (corrected UV mapping)
                texture_coords = self.mesh.point_data['UV']
                for vt in texture_coords:
                    # Don't flip V coordinate here since TextureMapper already handles it
                    f.write(f"vt {vt[0]} {vt[1]}\n")

                f.write("g TexturedMesh\n")
                f.write("usemtl material0\n")

                # Write faces
                face_index = 0
                while face_index < len(faces):
                    n_vertices = faces[face_index]
                    face_vertex_indices = faces[face_index + 1:face_index + 1 + n_vertices]
                    face_str = " ".join([f"{vi + 1}/{vi + 1}" for vi in face_vertex_indices])
                    f.write(f"f {face_str}\n")
                    face_index += n_vertices + 1

            self.logger.info(f"OBJ file saved as {output_filename}")
        except Exception as e:
            self.logger.error(f"Error saving OBJ file: {str(e)}", exc_info=True)
            raise

    def convert_and_save(self, obj_filename, texture_filename):
        """
        Convert the mesh to OBJ format and save all associated files.


        This method orchestrates the entire conversion process, including:
        1. Converting the mesh to OBJ format and saving it
        2. Generating and saving the texture image
        3. Creating and saving the Material Template Library (MTL) file

        The method ensures that all necessary files (OBJ, MTL, and texture image)
        are created and properly referenced to represent a complete textured 3D model.

        Args:
            obj_filename (str): The name of the output OBJ file. This should include
                                the full path if you want to save it in a specific directory.
            texture_filename (str): The name of the output texture image file. This should
                                    include the full path if you want to save it in a specific directory.

        Raises:
            Exception: If there's an error during any part of the conversion process.
                       This could include file I/O errors, texture generation errors,
                       or any other exceptions raised by the component methods.
        """
        try:
            self.convert_to_obj(obj_filename)
            self.save_texture_image(texture_filename)
            self.create_mtl_file(obj_filename, texture_filename)
            self.logger.info(f"OBJ file saved as {obj_filename}")
            self.logger.info(f"Texture image saved as {texture_filename}")
        except Exception as e:
            # self.logger.error(f"Error in convert_and_save: {str(e)}")
            self.logger.error(f"Error in convert_and_save: {str(e)}", exc_info=True)
            raise
