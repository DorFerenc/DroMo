import pytest
import numpy as np
from app import create_app
from app.db.mongodb import get_db
from app.models.threed_model import ThreeDModel
from app.models.point_cloud import PointCloud
from app.services.recon_proc_visualization_service import ReconProcVisualizationService
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'MONGODB_URI': 'mongodb://mongo:27017/dromo_test'
    })
    yield app

@pytest.fixture
def mongo(app):
    """Create a MongoDB test database and drop it after the test."""
    with app.app_context():
        db = get_db()
        yield db
        db.client.drop_database(db.name)

@pytest.fixture
def mock_threed_model():
    model = MagicMock(spec=ThreeDModel)
    model.id = 'test_model_id'
    model.point_cloud_id = 'test_point_cloud_id'
    model.obj_file = '/path/to/model.obj'
    model.texture_file = '/path/to/texture.jpg'
    return model

@pytest.fixture
def mock_point_cloud():
    point_cloud = MagicMock(spec=PointCloud)
    point_cloud.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    point_cloud.colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
    return point_cloud

def test_numpy_to_python():
    """
    Scenario: Convert numpy types to Python types
        Given I have various numpy data types
        When I convert them using numpy_to_python method
        Then I should get equivalent Python types
    """
    assert ReconProcVisualizationService.numpy_to_python(np.int64(5)) == 5
    assert ReconProcVisualizationService.numpy_to_python(np.float64(3.14)) == 3.14
    assert ReconProcVisualizationService.numpy_to_python(np.array([1, 2, 3])) == [1, 2, 3]
    assert ReconProcVisualizationService.numpy_to_python("test") == "test"

def test_get_point_cloud_data(app, mongo, mock_threed_model, mock_point_cloud):
    """
    Scenario: Retrieve point cloud data
        Given I have a 3D model with an associated point cloud
        When I call get_point_cloud_data method
        Then I should receive the point cloud data in the correct format
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.models.point_cloud.PointCloud.get_by_id', return_value=mock_point_cloud):
            result = ReconProcVisualizationService.get_point_cloud_data('test_model_id')

    assert result['type'] == 'scatter3d'
    assert result['mode'] == 'markers'
    assert result['x'] == [1, 4, 7]
    assert result['y'] == [2, 5, 8]
    assert result['z'] == [3, 6, 9]
    assert result['marker']['size'] == 1.5
    assert result['marker']['color'] == [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    assert result['marker']['opacity'] == 1

def test_get_mesh_data(app, mongo, mock_threed_model):
    """
    Scenario: Retrieve mesh data
        Given I have a 3D model
        When I call get_mesh_data method
        Then I should receive the mesh data in the correct format
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.services.recon_proc_visualization_service.pv.read') as mock_pv_read:
            mock_mesh = MagicMock()
            mock_mesh.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            mock_mesh.faces = np.array([[3, 0, 1, 2]])
            mock_pv_read.return_value = mock_mesh

            result = ReconProcVisualizationService.get_mesh_data('test_model_id', mesh_type='initial')

    assert len(result) == 2
    surface = result[0]
    wireframe = result[1]

    assert surface['type'] == 'mesh3d'
    assert surface['x'] == [1, 4, 7]
    assert surface['y'] == [2, 5, 8]
    assert surface['z'] == [3, 6, 9]
    assert surface['i'] == [0]
    assert surface['j'] == [1]
    assert surface['k'] == [2]
    assert surface['color'] == 'rgb(255, 165, 0)'

    assert wireframe['type'] == 'scatter3d'
    assert wireframe['mode'] == 'lines'
    assert len(wireframe['x']) == 9  # 3 lines * 3 points (including None)
    assert len(wireframe['y']) == 9
    assert len(wireframe['z']) == 9

def test_get_textured_mesh_data(app, mongo, mock_threed_model):
    """
    Scenario: Retrieve textured mesh data
        Given I have a 3D model with texture
        When I call get_textured_mesh_data method
        Then I should receive the textured mesh data in the correct format
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.services.recon_proc_visualization_service.pv.read') as mock_pv_read:
            mock_mesh = MagicMock()
            mock_mesh.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            mock_mesh.faces = np.array([[3, 0, 1, 2]])
            mock_mesh.active_t_coords = np.array([[0, 0], [0.5, 0.5], [1, 1]])
            mock_pv_read.return_value = mock_mesh

            with patch('app.services.recon_proc_visualization_service.Image.open') as mock_image_open:
                mock_texture = MagicMock()
                mock_texture_array = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]])
                mock_image_open.return_value = mock_texture
                mock_texture.__array__ = lambda: mock_texture_array

                result = ReconProcVisualizationService.get_textured_mesh_data('test_model_id')

    assert len(result) == 1
    mesh = result[0]

    assert mesh['type'] == 'mesh3d'
    assert mesh['x'] == [1, 4, 7]
    assert mesh['y'] == [2, 5, 8]
    assert mesh['z'] == [3, 6, 9]
    assert mesh['i'] == [0]
    assert mesh['j'] == [1]
    assert mesh['k'] == [2]

    expected_colors = [[0, 0, 255], [255, 0, 0], [0, 255, 0]]
    assert np.array_equal(mesh['vertexcolor'], expected_colors)

    # Check if the colors match the actual mapping
    assert np.array_equal(mesh['vertexcolor'][0], mock_texture_array[1, 0])  # (0, 0) -> [0, 0, 255]
    assert np.array_equal(mesh['vertexcolor'][1], mock_texture_array[0, 0])  # (0.5, 0.5) -> [255, 0, 0]
    assert np.array_equal(mesh['vertexcolor'][2], mock_texture_array[0, 1])  # (1, 1) -> [0, 255, 0]

    # Print additional information for debugging
    print(f"Actual vertexcolor: {mesh['vertexcolor']}")
    print(f"Texture coordinates: {mock_mesh.active_t_coords}")
    print(f"Texture array: {mock_texture_array}")
    print(f"Mapping:")
    print(f"  (0, 0) -> {mock_texture_array[1, 0]}")
    print(f"  (0.5, 0.5) -> {mock_texture_array[0, 0]}")
    print(f"  (1, 1) -> {mock_texture_array[0, 1]}")

def test_get_mesh_data_refined(app, mongo, mock_threed_model):
    """
    Scenario: Retrieve refined mesh data
        Given I have a 3D model
        When I call get_mesh_data method with mesh_type='refined'
        Then I should receive the refined mesh data with the correct color
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.services.recon_proc_visualization_service.pv.read') as mock_pv_read:
            mock_mesh = MagicMock()
            mock_mesh.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            mock_mesh.faces = np.array([[3, 0, 1, 2]])
            mock_pv_read.return_value = mock_mesh

            result = ReconProcVisualizationService.get_mesh_data('test_model_id', mesh_type='refined')

    assert len(result) == 2
    surface = result[0]

    assert surface['type'] == 'mesh3d'
    assert surface['color'] == 'rgb(255, 140, 0)'  # Check for refined mesh color

def test_get_point_cloud_data_no_colors(app, mongo, mock_threed_model, mock_point_cloud):
    """
    Scenario: Retrieve point cloud data without colors
        Given I have a 3D model with an associated point cloud without color information
        When I call get_point_cloud_data method
        Then I should receive the point cloud data with default color
    """
    mock_point_cloud.colors = None
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.models.point_cloud.PointCloud.get_by_id', return_value=mock_point_cloud):
            result = ReconProcVisualizationService.get_point_cloud_data('test_model_id')

    assert result['type'] == 'scatter3d'
    assert result['mode'] == 'markers'
    assert result['marker']['color'] == 'rgb(100, 100, 100)'  # Check for default color

def test_get_textured_mesh_data_no_texture_coords(app, mongo, mock_threed_model):
    """
    Scenario: Retrieve textured mesh data without texture coordinates
        Given I have a 3D model without texture coordinates
        When I call get_textured_mesh_data method
        Then I should receive the mesh data with default color
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.services.recon_proc_visualization_service.pv.read') as mock_pv_read:
            mock_mesh = MagicMock()
            mock_mesh.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            mock_mesh.faces = np.array([[3, 0, 1, 2]])
            mock_mesh.active_t_coords = None
            mock_pv_read.return_value = mock_mesh

            with patch('app.services.recon_proc_visualization_service.Image.open') as mock_image_open:
                mock_texture = MagicMock()
                mock_texture_array = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]])
                mock_image_open.return_value = mock_texture
                mock_texture.__array__ = lambda: mock_texture_array

                result = ReconProcVisualizationService.get_textured_mesh_data('test_model_id')

    assert len(result) == 1
    mesh = result[0]

    assert mesh['type'] == 'mesh3d'
    assert np.array_equal(mesh['vertexcolor'], [[200, 200, 200], [200, 200, 200], [200, 200, 200]])  # Check for default color

def test_get_mesh_data_invalid_type(app, mongo, mock_threed_model):
    """
    Scenario: Attempt to retrieve mesh data with an invalid mesh type
        Given I have a 3D model
        When I call get_mesh_data method with an invalid mesh_type
        Then I should receive mesh data with the default color
    """
    with patch('app.models.threed_model.ThreeDModel.get_by_id', return_value=mock_threed_model):
        with patch('app.services.recon_proc_visualization_service.pv.read') as mock_pv_read:
            mock_mesh = MagicMock()
            mock_mesh.points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            mock_mesh.faces = np.array([[3, 0, 1, 2]])
            mock_pv_read.return_value = mock_mesh

            result = ReconProcVisualizationService.get_mesh_data('test_model_id', mesh_type='invalid_type')

    assert len(result) == 2
    surface = result[0]

    assert surface['type'] == 'mesh3d'
    assert surface['color'] == 'rgb(100, 100, 100)'  # Check for default color

if __name__ == '__main__':
    pytest.main()