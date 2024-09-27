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
from unittest.mock import patch

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

def test_reconstruct_success(client, mongo):
    """
    Scenario: Successfully reconstruct a point cloud
        Given I have a point cloud in the database
        When I send a POST request to reconstruct the point cloud
        Then I should receive a success response with a model ID
    """
    # Create a test point cloud
    pc_string = """x,y,z,r,g,b
    0.1,0.2,0.3,255,0,0
    0.4,0.5,0.6,0,255,0"""
    pc = PointCloud.from_string("Test Cloud", pc_string)
    pc_id = pc.save()

    # Mock the ReconstructionService.start_reconstruction method
    with patch.object(ReconstructionService, 'start_reconstruction', return_value='mock_model_id') as mock_reconstruct:
        response = client.post(f'/api/reconstruct/{pc_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Reconstruction completed successfully"
    assert data['model_id'] == 'mock_model_id'
    mock_reconstruct.assert_called_once_with(str(pc_id))

def test_reconstruct_not_found(client, mongo):
    """
    Scenario: Attempt to reconstruct a non-existent point cloud
        Given I have an invalid point cloud ID
        When I send a POST request to reconstruct the point cloud
        Then I should receive a not found error response
    """
    invalid_id = str(ObjectId())
    response = client.post(f'/api/reconstruct/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "Point cloud not found" in data['error']

def test_reconstruct_server_error(client, mongo):
    """
    Scenario: Server error during reconstruction
        Given I have a valid point cloud in the database
        When I send a POST request to reconstruct the point cloud
        And an unexpected error occurs during reconstruction
        Then I should receive a server error response
    """
    # Create a test point cloud
    pc_string = """x,y,z,r,g,b
    0.1,0.2,0.3,255,0,0
    0.4,0.5,0.6,0,255,0"""
    pc = PointCloud.from_string("Test Cloud", pc_string)
    pc_id = pc.save()

    # Mock the ReconstructionService to raise an exception
    with patch.object(ReconstructionService, 'start_reconstruction', side_effect=Exception("Unexpected error")):
        response = client.post(f'/api/reconstruct/{pc_id}')

    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data
    assert data['error'] == "Internal server error"

# Add these new test functions

def test_reconstruct_with_parameters(client, mongo):
    """
    Scenario: Reconstruct with different parameters
    """
    pc_string = """x,y,z,r,g,b
    0.1,0.2,0.3,255,0,0
    0.4,0.5,0.6,0,255,0
    0.7,0.8,0.9,0,0,255
    1.0,1.1,1.2,255,255,255
    """
    pc = PointCloud.from_string("Test Cloud", pc_string)
    pc_id = pc.save()

    params = {
        'resolution': 'high',
        'smoothing': 0.5
    }
    response = client.post(f'/api/reconstruct/{pc_id}', json=params)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'model_id' in data