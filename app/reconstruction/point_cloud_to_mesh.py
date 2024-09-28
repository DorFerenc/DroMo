import numpy as np
import pyvista as pv
pv.OFF_SCREEN = True  # Disable the need for graphical output
import logging
import os
from scipy.spatial import cKDTree

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
from scipy.ndimage import laplace

class PointCloudToMesh:
    """
    A class to convert point cloud data to a 3D mesh.

    This class provides functionality to load point cloud data,
    generate a 3D mesh using Delaunay triangulation, and apply various smoothing
    and refinement techniques to improve the mesh quality.

    Attributes:
        point_cloud (np.ndarray): The loaded point cloud data.
        mesh (pv.PolyData): The generated 3D mesh.
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self):
        """Initialize the PointCloudToMesh object."""
        self.point_cloud = None
        self.mesh = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_point_cloud(self, points):
        """
        Set the point cloud data.

        Args:
            points (list or np.ndarray): Array of 3D point coordinates.
        """
        if len(points) == 0:
            raise ValueError("Point cloud cannot be empty")
        # Convert to numpy array if it's not already
        if not isinstance(points, np.ndarray):
            points = np.array(points)
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Point cloud must be a 2D array with 3 columns (x, y, z)")
        self.point_cloud = points
        self.logger.info(f"Point cloud set with {len(points)} points")

    def calculate_optimal_alpha(self, percentile=95):
        """
        Calculate an optimal alpha value for mesh generation based on point cloud characteristics.

        This method uses the distance to the nearest neighbor for each point to estimate
        an appropriate alpha value. It aims to create a mesh that captures the shape of the
        point cloud without creating too many artifacts or holes.

        Args:
            percentile (int): Percentile of nearest neighbor distances to use for alpha calculation.
                              Default is 95, which works well for most point clouds.

        Returns:
            float: The calculated optimal alpha value.
        """
        if self.point_cloud is None or len(self.point_cloud) < 2:
            raise ValueError("Point cloud not set or has insufficient points")

        self.logger.info("Calculating optimal alpha value...")

        # Build a KD-tree for efficient nearest neighbor search
        tree = cKDTree(self.point_cloud)

        # Find the distance to the nearest neighbor for each point
        distances, _ = tree.query(self.point_cloud, k=2)  # k=2 because the nearest neighbor of a point is itself
        nearest_neighbor_distances = distances[:, 1]  # Take the second-nearest neighbor (first is the point itself)

        # Calculate the alpha value based on the specified percentile of nearest neighbor distances
        alpha = np.percentile(nearest_neighbor_distances, percentile)

        # Apply a scaling factor to fine-tune the alpha value
        # This factor can be adjusted based on empirical results
        if self.is_cube_like():
            scaling_factor = 25.2
        else:
            scaling_factor = 2.2
        # alpha *= scaling_factor
        # scaling_factor = 2.0
        alpha *= scaling_factor

        self.logger.info(f"Calculated optimal alpha: {alpha:.6f}")
        return alpha

    # Overwrite to cube like stuff
    def is_cube_like(self):
        # Check if the point cloud resembles a cube
        min_coords = np.min(self.point_cloud, axis=0)
        max_coords = np.max(self.point_cloud, axis=0)
        dimensions = max_coords - min_coords
        aspect_ratios = dimensions / np.max(dimensions)
        return np.all(aspect_ratios > 0.8)  # Consider it cube-like if all dimensions are similar

    def generate_mesh(self, alpha=None):
        """
        Generate a 3D mesh from the loaded point cloud data using Delaunay triangulation.

        Args:
            alpha (float, optional): The alpha value for the Delaunay triangulation algorithm.
                                     If None, calculates the optimal alpha value.

        Raises:
            ValueError: If no point cloud data has been loaded.
        """
        if self.point_cloud is None:
            self.logger.error("No point cloud data loaded")
            raise ValueError("No point cloud data loaded. Use set_point_cloud() first.")
        if len(self.point_cloud) < 4:
            raise ValueError("At least 4 points are required to generate a 3D mesh")

        if alpha is None:
            alpha = self.calculate_optimal_alpha()

        self.logger.info(f"Generating mesh with alpha={alpha}")
        try:
            poly_data = pv.PolyData(self.point_cloud)
            self.mesh = poly_data.delaunay_3d(alpha=alpha)
            self.mesh = self.mesh.extract_surface()

            # Remove degenerate triangles
            self.mesh.clean(tolerance=1e-6)

            n_cells = self.mesh.n_cells
            self.logger.info(f"Mesh generated with {self.mesh.n_points} points and {n_cells} cells")

            # Compute and log mesh quality
            self.log_mesh_quality()
            return self.mesh
        except Exception as e:
            self.logger.error(f"Error generating mesh: {str(e)}")
            raise

    def log_mesh_quality(self):
        """
        Compute and log the quality metrics of the generated mesh.

        This method calculates various quality metrics for the mesh cells, including
        minimum, maximum, and average quality values. These metrics help assess the
        overall quality of the generated mesh and can be used to identify potential
        issues or areas for improvement in the mesh generation process.

        The quality metric used is based on the ratio of the inscribed sphere radius
        to the circumscribed sphere radius for each cell, scaled to [0, 1].

        If the mesh has no cells, a warning is logged instead.

        Note:
            This method assumes that the mesh has already been generated and stored
            in the `self.mesh` attribute.

        Raises:
            AttributeError: If `self.mesh` is None or doesn't have the required methods.
        """
        quality = self.mesh.compute_cell_quality()
        quality_array = quality['CellQuality']
        if len(quality_array) > 0:
            min_quality = np.min(quality_array)
            max_quality = np.max(quality_array)
            avg_quality = np.mean(quality_array)
            self.logger.info(
                f"Mesh quality - Min: {min_quality:.4f}, Max: {max_quality:.4f}, Avg: {avg_quality:.4f}")
        else:
            self.logger.warning("Unable to compute mesh quality. No cells in the mesh.")

    def visualize_mesh(self):
        """
        Visualize the generated mesh.

        Raises:
            ValueError: If no mesh has been generated.
        """
        if self.mesh is None:
            raise ValueError("No mesh generated. Use generate_mesh() first.")

        p = pv.Plotter()
        p.add_mesh(self.mesh, color='orange')
        p.show()

    def save_mesh(self, filename):
        """
        Save the generated mesh to a file.

        Args:
            filename (str): The name of the file to save the mesh to.
                            Supported formats: .ply, .vtp, .stl, .vtk

        Raises:
            ValueError: If no mesh has been generated or if the file extension is not supported.
        """
        if self.mesh is None:
            self.logger.error("No mesh generated to save")
            raise ValueError("No mesh generated. Use generate_mesh() first.")

        supported_extensions = ['.ply', '.vtp', '.stl', '.vtk']
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in supported_extensions:
            self.logger.error(f"Unsupported file extension. Supported formats: {', '.join(supported_extensions)}")
            raise ValueError(f"Unsupported file extension. Supported formats: {', '.join(supported_extensions)}")

        try:
            self.mesh.save(filename)
            self.logger.info(f"Mesh saved successfully to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving mesh: {str(e)}")
            raise


##########################################
# OPTIONAL FOR UPGRADE
###########################################
# class MeshRefiner:
#     @staticmethod
#     def refine_mesh(mesh):
#         # Implement mesh refinement techniques here
#         # For example:
#         # refined_mesh = mesh.smooth(n_iter=100, relaxation_factor=0.1)
#         # return refined_mesh
#         return mesh  # Placeholder, replace with actual refinement logic

class MeshRefiner:
    def __init__(self, mesh):
        self.mesh = mesh
        self.logger = logging.getLogger(self.__class__.__name__)
        self.original_type = type(mesh)

    def _to_polydata(self):
        if not isinstance(self.mesh, pv.PolyData):
            self.logger.info("Converting mesh to PolyData for processing")
            if isinstance(self.mesh, pv.UnstructuredGrid):
                self.mesh = self.mesh.extract_surface()
            else:
                self.mesh = pv.PolyData(self.mesh.points, self.mesh.faces)

    def _restore_original_type(self):
        if self.original_type != type(self.mesh):
            self.logger.info(f"Restoring mesh to original type: {self.original_type.__name__}")
            if self.original_type == pv.UnstructuredGrid:
                self.mesh = pv.UnstructuredGrid(self.mesh)

    def smooth(self, n_iter=5, relaxation_factor=0.01, feature_smoothing=False, boundary_smoothing=True):
        """Apply gentle Laplacian smoothing to the mesh while preserving features."""
        self.logger.info(f"Applying gentle Laplacian smoothing with {n_iter} iterations")
        self._to_polydata()
        try:
            self.mesh = self.mesh.smooth(
                n_iter=n_iter,
                relaxation_factor=relaxation_factor,
                feature_smoothing=feature_smoothing,
                boundary_smoothing=boundary_smoothing,
                edge_angle=15,
                feature_angle=60
            )
        except Exception as e:
            self.logger.warning(f"Error smoothing mesh: {str(e)}. Skipping this step.")
        return self.mesh

    def clean(self, tolerance=1e-6):
        """Clean the mesh by merging duplicate points and removing unused points."""
        self.logger.info(f"Cleaning mesh with tolerance {tolerance}")
        self._to_polydata()
        try:
            self.mesh = self.mesh.clean(tolerance=tolerance)
        except Exception as e:
            self.logger.warning(f"Error cleaning mesh: {str(e)}. Skipping this step.")
        return self.mesh

    def remove_small_components(self, min_ratio=0.01):
        """Remove small disconnected components from the mesh."""
        self.logger.info(f"Removing small components with min_ratio {min_ratio}")
        self._to_polydata()
        try:
            conn = self.mesh.connectivity()
            labels = conn.cell_data["RegionId"]
            unique_labels, counts = np.unique(labels, return_counts=True)
            max_count = counts.max()
            keep_labels = unique_labels[counts >= max_count * min_ratio]
            mask = np.isin(labels, keep_labels)
            self.mesh = self.mesh.extract_cells(mask)
        except Exception as e:
            self.logger.warning(f"Error removing small components: {str(e)}. Skipping this step.")
        return self.mesh

    def fill_holes(self, max_hole_size=None):
        """Fill holes in the mesh surface."""
        self.logger.info(f"Filling holes up to size {max_hole_size}")
        self._to_polydata()
        try:
            # First, try PyVista's built-in method
            self.mesh = self.mesh.fill_holes(max_hole_size)

            # Then, use a custom approach for any remaining holes
            edges = self.mesh.extract_feature_edges(feature_angle=60, boundary_edges=True, non_manifold_edges=False)
            if edges.n_cells > 0:
                hole_fill = edges.triangulate()
                self.mesh = self.mesh.boolean_union(hole_fill)
        except Exception as e:
            self.logger.warning(f"Error filling holes: {str(e)}. Skipping this step.")
        return self.mesh

    def remove_degenerate_faces(self, tolerance=1e-6):
        """Remove degenerate faces from the mesh."""
        self.logger.info(f"Removing degenerate faces with tolerance {tolerance}")
        self._to_polydata()
        try:
            areas = self.mesh.compute_cell_sizes()["Area"]
            mask = areas > tolerance
            self.mesh = self.mesh.extract_cells(mask)
        except Exception as e:
            self.logger.warning(f"Error removing degenerate faces: {str(e)}. Skipping this step.")
        return self.mesh

    def ensure_watertight(self):
        """Ensure the mesh is watertight."""
        self.logger.info("Ensuring mesh is watertight")
        self._to_polydata()
        try:
            # Extract the outer surface
            surface = self.mesh.extract_surface()
            # Fill any remaining holes
            filled = surface.fill_holes(1000)  # Use a large max_hole_size to fill all holes
            # Triangulate to ensure a consistent surface
            self.mesh = filled.triangulate()
        except Exception as e:
            self.logger.warning(f"Error ensuring watertight mesh: {str(e)}. Skipping this step.")
        return self.mesh

    def refine(self):
        """Apply a complete refinement pipeline to the mesh."""
        self.logger.info("Starting complete mesh refinement pipeline")

        # Initial cleaning
        self.clean(tolerance=1e-6)

        # Remove small disconnected components
        self.remove_small_components(min_ratio=0.01)

        # Fill holes (more aggressive)
        self.fill_holes(max_hole_size=None)  # Fill all holes

        # Remove degenerate faces
        # self.remove_degenerate_faces(tolerance=1e-6)

        # Apply very gentle smoothing
        self.smooth(n_iter=3, relaxation_factor=0.01, feature_smoothing=False, boundary_smoothing=True)

        # Ensure the mesh is watertight
        self.ensure_watertight()

        # Final cleaning pass
        self.clean(tolerance=1e-6)

        # Restore original mesh type if changed
        self._restore_original_type()

        self.logger.info("Mesh refinement pipeline completed")
        return self.mesh

    def get_refined_mesh(self):
        """Get the current state of the refined mesh."""
        return self.mesh
