import pytest
from app import create_app
from app.db.mongodb import get_db
from app.models.threed_model import ThreeDModel
from app.models.point_cloud import PointCloud
from app.services.recon_proc_visualization_service import ReconProcVisualizationService
import json
from unittest.mock import patch
from bson import ObjectId

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

def test_get_point_cloud_data_success(client, mongo):
    """
    Scenario: Successfully retrieve point cloud data
        Given I have a 3D model with an associated point cloud in the database
        When I send a GET request to retrieve the point cloud data
        Then I should receive a success response with the point cloud data
    """
    # Create a test point cloud and 3D model
    pc_string = """x,y,z,r,g,b
    0.1,0.2,0.3,255,0,0
    0.4,0.5,0.6,0,255,0"""
    pc = PointCloud.from_string("Test Cloud", pc_string)
    pc_id = pc.save()

    model = ThreeDModel(name="Test Model", folder_path="/test/path", point_cloud_id=pc_id,
                        obj_file="/test/model.obj", mtl_file="/test/model.mtl", texture_file="/test/texture.jpg")
    model_id = model.save()

    # Mock the ReconProcVisualizationService.get_point_cloud_data method
    mock_data = {
        'type': 'scatter3d',
        'mode': 'markers',
        'x': [0.1, 0.4],
        'y': [0.2, 0.5],
        'z': [0.3, 0.6],
        'marker': {'size': 1.5, 'color': [[255, 0, 0], [0, 255, 0]], 'opacity': 1}
    }
    with patch.object(ReconProcVisualizationService, 'get_point_cloud_data', return_value=mock_data):
        response = client.get(f'/api/reconstruction/point_cloud/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [mock_data]

def test_get_point_cloud_data_not_found(client, mongo):
    """
    Scenario: Attempt to retrieve point cloud data for a non-existent model
        Given I have an invalid model ID
        When I send a GET request to retrieve the point cloud data
        Then I should receive a not found error response
    """
    invalid_id = str(ObjectId())  # Generate a valid ObjectId that doesn't exist in the database
    response = client.get(f'/api/reconstruction/point_cloud/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Model or point cloud not found" in data['error']

def test_get_initial_mesh_data_success(client, mongo):
    """
    Scenario: Successfully retrieve initial mesh data
        Given I have a 3D model in the database
        When I send a GET request to retrieve the initial mesh data
        Then I should receive a success response with the initial mesh data
    """
    # Create a test 3D model
    model = ThreeDModel(name="Test Model", folder_path="/test/path", point_cloud_id="test_pc_id",
                        obj_file="/test/model.obj", mtl_file="/test/model.mtl", texture_file="/test/texture.jpg")
    model_id = model.save()

    # Mock the ReconProcVisualizationService.get_mesh_data method
    mock_data = [
        {
            'type': 'mesh3d',
            'x': [1, 2, 3],
            'y': [4, 5, 6],
            'z': [7, 8, 9],
            'i': [0, 1, 2],
            'j': [1, 2, 0],
            'k': [2, 0, 1],
            'color': 'rgb(255, 165, 0)',
            'flatshading': True,
        },
        {
            'type': 'scatter3d',
            'mode': 'lines',
            'x': [1, 2, None, 2, 3, None, 3, 1, None],
            'y': [4, 5, None, 5, 6, None, 6, 4, None],
            'z': [7, 8, None, 8, 9, None, 9, 7, None],
            'line': {'color': 'rgb(0, 0, 0)', 'width': 1},
        }
    ]
    with patch.object(ReconProcVisualizationService, 'get_mesh_data', return_value=mock_data):
        response = client.get(f'/api/reconstruction/initial_mesh/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == mock_data

def test_get_initial_mesh_data_not_found(client, mongo):
    """
    Scenario: Attempt to retrieve initial mesh data for a non-existent model
        Given I have an invalid model ID
        When I send a GET request to retrieve the initial mesh data
        Then I should receive a not found error response
    """
    invalid_id = str(ObjectId())  # Generate a valid ObjectId that doesn't exist in the database
    response = client.get(f'/api/reconstruction/initial_mesh/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Model not found" in data['error']

# Add similar tests for refined mesh and textured mesh endpoints

def test_get_textured_mesh_data_success(client, mongo):
    """
    Scenario: Successfully retrieve textured mesh data
        Given I have a 3D model with texture in the database
        When I send a GET request to retrieve the textured mesh data
        Then I should receive a success response with the textured mesh data
    """
    # Create a test 3D model
    model = ThreeDModel(name="Test Model", folder_path="/test/path", point_cloud_id="test_pc_id",
                        obj_file="/test/model.obj", mtl_file="/test/model.mtl", texture_file="/test/texture.jpg")
    model_id = model.save()

    # Mock the ReconProcVisualizationService.get_textured_mesh_data method
    mock_data = [{
        'type': 'mesh3d',
        'x': [1, 2, 3],
        'y': [4, 5, 6],
        'z': [7, 8, 9],
        'i': [0, 1, 2],
        'j': [1, 2, 0],
        'k': [2, 0, 1],
        'vertexcolor': [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        'flatshading': False,
    }]
    with patch.object(ReconProcVisualizationService, 'get_textured_mesh_data', return_value=mock_data):
        response = client.get(f'/api/reconstruction/textured_mesh/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == mock_data

def test_get_textured_mesh_data_not_found(client, mongo):
    """
    Scenario: Attempt to retrieve textured mesh data for a non-existent model
        Given I have an invalid model ID
        When I send a GET request to retrieve the textured mesh data
        Then I should receive a not found error response
    """
    invalid_id = str(ObjectId())  # Generate a valid ObjectId that doesn't exist in the database
    response = client.get(f'/api/reconstruction/textured_mesh/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Model not found" in data['error']