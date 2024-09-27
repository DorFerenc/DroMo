import pytest
from app import create_app
from app.db.mongodb import get_db
from app.models.threed_model import ThreeDModel
from app.models.point_cloud import PointCloud
import json
import os
from bson import ObjectId
from unittest.mock import patch
import pyvista as pv

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

def test_get_point_cloud_data(client, mongo):
    """
    Scenario: Get point cloud data for visualization
    """
    pc = PointCloud("Test Cloud", np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]]))
    pc_id = pc.save()
    model = ThreeDModel("Test Model", "test_folder", pc_id, "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.get(f'/api/reconstruction/point_cloud/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'x' in data[0] and 'y' in data[0] and 'z' in data[0]

@patch('pyvista.read')
def test_get_initial_mesh_data(client, mongo):
    """
    Scenario: Get initial mesh data for visualization
    """
    model = ThreeDModel("Test Model", "test_folder", "pc_id", "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.get(f'/api/reconstruction/initial_mesh/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vertices' in data
    assert 'faces' in data

def test_get_refined_mesh_data(client, mongo):
    """
    Scenario: Get refined mesh data for visualization
    """
    model = ThreeDModel("Test Model", "test_folder", "pc_id", "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.get(f'/api/reconstruction/refined_mesh/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vertices' in data
    assert 'faces' in data

def test_get_textured_mesh_data(client, mongo):
    """
    Scenario: Get textured mesh data for visualization
    """
    model = ThreeDModel("Test Model", "test_folder", "pc_id", "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.get(f'/api/reconstruction/textured_mesh/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vertices' in data
    assert 'faces' in data
    assert 'uv' in data

def test_nonexistent_model_visualization(client):
    """
    Scenario: Attempt to get visualization data for a non-existent model
    """
    nonexistent_id = str(ObjectId())

    endpoints = [
        f'/api/reconstruction/point_cloud/{nonexistent_id}',
        f'/api/reconstruction/initial_mesh/{nonexistent_id}',
        f'/api/reconstruction/refined_mesh/{nonexistent_id}',
        f'/api/reconstruction/textured_mesh/{nonexistent_id}'
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
        assert "Model or point cloud not found" in data['error']

def test_incomplete_model_visualization(client, mongo):
    """
    Scenario: Attempt to get visualization data for an incomplete model
    """
    incomplete_model = ThreeDModel("Incomplete Model", "test_folder", "pc_id", None, None, None)
    model_id = incomplete_model.save()

    endpoints = [
        f'/api/reconstruction/initial_mesh/{model_id}',
        f'/api/reconstruction/refined_mesh/{model_id}',
        f'/api/reconstruction/textured_mesh/{model_id}'
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "Model not found" in data['error']