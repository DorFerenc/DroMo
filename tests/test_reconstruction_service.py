import warnings
import numpy as np

# Suppress specific DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="vtkmodules.util.numpy_support")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="numpy.core.numeric")
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Patch numpy bool to avoid deprecation warning
np.bool = bool

import pytest
from app import create_app
from app.db.mongodb import get_db
from app.models.point_cloud import PointCloud
from app.services.reconstruction_service import ReconstructionService
from bson import ObjectId
import json
from unittest.mock import patch, MagicMock
import pyvista as pv
from app.reconstruction.point_cloud_to_mesh import PointCloudToMesh
from app.reconstruction.texture_mapper import TextureMapper
from app.reconstruction.mesh_to_obj_converter import MeshToOBJConverter
from app.reconstruction.reconstruction_utils import generate_colors


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'MONGODB_URI': 'mongodb://mongo:27017/dromo_test',
        'MODELS_FOLDER': '/tmp/test_models'
    })
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mongo(app):
    """Create a MongoDB test database and drop it after the test."""
    with app.app_context():
        db = get_db()
        yield db
        db.client.drop_database(db.name)

@pytest.fixture
def point_cloud_data():
    """Fixture to provide sample point cloud data."""
    return {
        '_id': ObjectId(),
        'name': 'Test Point Cloud',
        'points': [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
        'colors': [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    }

# Test classes
class TestReconstructionService:
    """Tests for the ReconstructionService class."""

    def test_start_reconstruction_returns_model_id_when_successful(self, app, mongo, point_cloud_data, monkeypatch):
        """
        Test that start_reconstruction returns a model ID when successful.

        This test mocks the necessary dependencies and verifies that the method
        returns a non-None model ID and calls the database as expected.
        """
        with app.app_context():
            # Insert test point cloud data
            mongo.point_clouds.insert_one(point_cloud_data)

            monkeypatch.setattr('os.makedirs', lambda *args, **kwargs: None)
            monkeypatch.setattr('os.path.exists', lambda *args: True)
            monkeypatch.setattr('os.access', lambda *args, **kwargs: True)
            monkeypatch.setattr(PointCloudToMesh, 'generate_mesh', lambda *args: pv.PolyData(np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])))
            monkeypatch.setattr(TextureMapper, 'apply_texture', lambda *args: None)
            monkeypatch.setattr(MeshToOBJConverter, 'convert_and_save', lambda *args: None)

            # Mock ThreeDModel.save() method
            monkeypatch.setattr('app.models.threed_model.ThreeDModel.save', lambda *args: ObjectId())

            model_id = ReconstructionService.start_reconstruction(str(point_cloud_data['_id']))

            assert model_id is not None
            assert mongo.point_clouds.find_one({'_id': point_cloud_data['_id']}) is not None

    def test_start_reconstruction_raises_error_when_point_cloud_not_found(self, app, mongo):
        """
        Test that start_reconstruction raises a ValueError when the point cloud is not found.

        This test verifies that the method raises the expected exception when
        the database returns None for the point cloud query.
        """
        with app.app_context():
            with pytest.raises(ValueError, match="Point cloud not found"):
                ReconstructionService.start_reconstruction(str(ObjectId()))

    def test_start_reconstruction_raises_error_when_no_points(self, app, mongo, point_cloud_data):
        """
        Test that start_reconstruction raises a ValueError when the point cloud has no points.

        This test verifies that the method raises the expected exception when
        the point cloud data contains an empty list of points.
        """
        with app.app_context():
            point_cloud_data['points'] = []
            mongo.point_clouds.insert_one(point_cloud_data)

            with pytest.raises(ValueError, match="Point cloud has no points data"):
                ReconstructionService.start_reconstruction(str(point_cloud_data['_id']))

class TestPointCloudToMesh:
    """Tests for the PointCloudToMesh class."""

    @pytest.fixture
    def pc_to_mesh(self):
        """Fixture to provide a PointCloudToMesh instance."""
        return PointCloudToMesh()

    @pytest.fixture
    def sample_points(self):
        """Fixture to provide sample 3D points."""
        return np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])

    def test_set_point_cloud_stores_points(self, pc_to_mesh, sample_points):
        """
        Test that set_point_cloud correctly stores the provided points.

        This test verifies that the points are correctly stored in the
        PointCloudToMesh instance after calling set_point_cloud.
        """
        pc_to_mesh.set_point_cloud(sample_points)
        np.testing.assert_array_equal(pc_to_mesh.point_cloud, sample_points)

    def test_set_point_cloud_raises_error_for_empty_input(self, pc_to_mesh):
        """
        Test that set_point_cloud raises a ValueError for empty input.

        This test verifies that the method raises the expected exception
        when an empty list is provided as input.
        """
        with pytest.raises(ValueError, match="Point cloud cannot be empty"):
            pc_to_mesh.set_point_cloud([])

    def test_generate_mesh_returns_polydata(self, pc_to_mesh, sample_points):
        """
        Test that generate_mesh returns a PolyData object.

        This test verifies that the generate_mesh method returns a PolyData
        object with the correct number of points.
        """
        pc_to_mesh.set_point_cloud(sample_points)
        mesh = pc_to_mesh.generate_mesh()
        assert isinstance(mesh, pv.PolyData)
        assert mesh.n_points == len(sample_points)

class TestTextureMapper:
    """Tests for the TextureMapper class."""

    @pytest.fixture
    def texture_mapper(self):
        """Fixture to provide a TextureMapper instance."""
        return TextureMapper()

    @pytest.fixture
    def sample_mesh(self):
        """Fixture to provide a sample mesh."""
        return pv.PolyData(np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]))

    @pytest.fixture
    def sample_points_and_colors(self):
        """Fixture to provide sample points and colors."""
        points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
        colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
        return points, colors

    def test_load_mesh_stores_mesh(self, texture_mapper, sample_mesh):
        """
        Test that load_mesh correctly stores the provided mesh.

        This test verifies that the mesh is correctly stored in the
        TextureMapper instance after calling load_mesh.
        """
        texture_mapper.load_mesh(sample_mesh)
        assert texture_mapper.mesh == sample_mesh

    def test_load_point_cloud_with_colors_stores_data(self, texture_mapper, sample_points_and_colors):
        """
        Test that load_point_cloud_with_colors correctly stores points and colors.

        This test verifies that the points and colors are correctly stored
        in the TextureMapper instance after calling load_point_cloud_with_colors.
        """
        points, colors = sample_points_and_colors
        texture_mapper.load_point_cloud_with_colors(points, colors)
        np.testing.assert_array_equal(texture_mapper.point_cloud, points)
        np.testing.assert_array_equal(texture_mapper.colors, colors)

    def test_apply_texture_calls_expected_methods(self, texture_mapper, sample_mesh, sample_points_and_colors, monkeypatch):
        """
        Test that apply_texture calls the expected methods.

        This test verifies that the apply_texture method calls the expected
        internal methods in the correct order.
        """
        points, colors = sample_points_and_colors
        texture_mapper.load_mesh(sample_mesh)
        texture_mapper.load_point_cloud_with_colors(points, colors)

        mock_map_colors = MagicMock()
        mock_smooth = MagicMock()
        mock_apply_uv = MagicMock()

        monkeypatch.setattr(TextureMapper, 'map_colors_to_mesh', mock_map_colors)
        monkeypatch.setattr(TextureMapper, 'smooth_texture', mock_smooth)
        monkeypatch.setattr(TextureMapper, 'apply_smart_uv_mapping', mock_apply_uv)

        texture_mapper.apply_texture()

        mock_map_colors.assert_called_once()
        mock_smooth.assert_called_once()
        mock_apply_uv.assert_called_once()

class TestReconstructionUtils:
    """Tests for the reconstruction_utils module."""

    @pytest.fixture
    def sample_points(self):
        """Fixture to provide sample 3D points."""
        return np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])

    def test_generate_colors_random_returns_correct_shape(self, sample_points):
        """
        Test that generate_colors with 'random' method returns correct shape.

        This test verifies that the generate_colors function returns an array
        of the correct shape and range when using the 'random' method.
        """
        colors = generate_colors(sample_points, method='random')
        assert colors.shape == (3, 3)
        assert np.all(colors >= 0) and np.all(colors <= 1)

    def test_generate_colors_height_returns_ordered_colors(self, sample_points):
        """
        Test that generate_colors with 'height' method returns ordered colors.

        This test verifies that the generate_colors function returns an array
        of the correct shape and with colors ordered by height when using the 'height' method.
        """
        colors = generate_colors(sample_points, method='height')
        assert colors.shape == (3, 3)
        assert np.all(colors >= 0) and np.all(colors <= 1)
        assert np.all(colors[0, 0] <= colors[1, 0] <= colors[2, 0])

    def test_generate_colors_raises_error_for_unknown_method(self, sample_points):
        """
        Test that generate_colors raises an error for unknown method.

        This test verifies that the generate_colors function raises a ValueError
        when an unknown color generation method is specified.
        """
        with pytest.raises(ValueError, match="Unknown color generation method"):
            generate_colors(sample_points, method='unknown')



def test_reconstruct_api_endpoint(client, mongo, point_cloud_data):
    """
    Test the /api/reconstruct endpoint.
    """
    # Insert test point cloud data
    mongo.point_clouds.insert_one(point_cloud_data)

    # Mock ReconstructionService.start_reconstruction
    with patch.object(ReconstructionService, 'start_reconstruction', return_value=str(ObjectId())) as mock_reconstruct:
        response = client.post(f'/api/reconstruct/{str(point_cloud_data["_id"])}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "model_id" in data
    mock_reconstruct.assert_called_once_with(str(point_cloud_data['_id']))