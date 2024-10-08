import numpy as np
import os
import pytest
from app import create_app
from app.db.mongodb import get_db
from app.models.point_cloud import PointCloud
from app.services.preprocess_service import PreprocessService
from app.services.visual_data_service import VisualDataService
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

@pytest.fixture
def test_ply_file():
    """Path to the test PLY file."""
    return os.path.join(os.path.dirname(__file__), 'ply', 'input.ply')

def test_process_ply_success(client, mongo, test_ply_file):
    """
    Scenario: Successfully process a PLY file
        Given I have a PLY file in the database
        When I call the process_ply method
        Then I should receive a success response with a point cloud ID
    """
    # Create a test PLY file entry
    ply_id = str(ObjectId())
    mongo.ply_files.insert_one({
        '_id': ObjectId(ply_id),
        'file_path': test_ply_file,
        'title': 'Test PLY'
    })

    # Mock the visual_dataService.get_visual_data method
    with patch.object(VisualDataService, 'get_visual_data', return_value={'file_path': test_ply_file, 'title': 'Test PLY'}):
        result = PreprocessService.process_ply(ply_id)

    assert result is not None
    assert result['ply_id'] == ply_id
    assert result['processed'] is True
    assert 'point_cloud_id' in result

def test_process_ply_not_found(client, mongo):
    """
    Scenario: Attempt to process a non-existent PLY file
        Given I have an invalid PLY file ID
        When I call the process_ply method
        Then I should receive a None result
    """
    invalid_id = str(ObjectId())

    # Mock the visual_dataService.get_visual_data method to return None
    with patch.object(VisualDataService, 'get_visual_data', return_value=None):
        result = PreprocessService.process_ply(invalid_id)

    assert result is None

def test_get_progress_success(client, mongo):
    """
    Scenario: Successfully get progress of a processed PLY file
        Given I have a processed PLY file in the database
        When I call the get_progress method
        Then I should receive the correct progress information
    """
    ply_id = str(ObjectId())
    point_cloud_id = str(ObjectId())
    ply_file = {
        '_id': ObjectId(ply_id),
        'file_path': '/path/to/test.ply',
        'title': 'Test PLY',
        'processed': True,
        'point_cloud_id': point_cloud_id
    }

    # Mock the visual_dataService.get_visual_data method
    with patch.object(VisualDataService, 'get_visual_data', return_value=ply_file):
        result = PreprocessService.get_progress(ply_id)

    assert result is not None
    assert result['ply_id'] == ply_id
    assert result['processed'] is True
    assert result['point_cloud_id'] == point_cloud_id

def test_get_progress_not_found(client, mongo):
    """
    Scenario: Attempt to get progress of a non-existent PLY file
        Given I have an invalid PLY file ID
        When I call the get_progress method
        Then I should receive a None result
    """
    invalid_id = str(ObjectId())

    # Mock the visual_dataService.get_visual_data method to return None
    with patch.object(VisualDataService, 'get_visual_data', return_value=None):
        result = PreprocessService.get_progress(invalid_id)

    assert result is None

def test_get_progress_not_processed(client, mongo):
    """
    Scenario: Get progress of an unprocessed PLY file
        Given I have an unprocessed PLY file in the database
        When I call the get_progress method
        Then I should receive the correct progress information
    """
    ply_id = str(ObjectId())
    ply_file = {
        '_id': ObjectId(ply_id),
        'file_path': '/path/to/test.ply',
        'title': 'Test PLY',
        'processed': False
    }

    # Mock the visual_dataService.get_visual_data method
    with patch.object(VisualDataService, 'get_visual_data', return_value=ply_file):
        result = PreprocessService.get_progress(ply_id)

    assert result is not None
    assert result['ply_id'] == ply_id
    assert result['processed'] is False
    assert result['point_cloud_id'] is None


@pytest.fixture
def point_cloud_data():
    """Fixture to provide sample point cloud data."""
    return {
        '_id': ObjectId(),
        'name': 'Test Point Cloud',
        'points': [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
        'colors': [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    }

def test_get_preprocess_process_ply_success(client, mongo, point_cloud_data):
    """
    Test the /api/preprocess/<param>/<ply_id> endpoint.
    """
    # Insert test point cloud data
    mongo.point_clouds.insert_one(point_cloud_data)

    param = "filtered_ply"
    ply_id = str(point_cloud_data["_id"])

    mock_ply_data = {
        'type': 'scatter3d',
        'mode': 'markers',
        'x': [0, 1, 2],
        'y': [0, 1, 2],
        'z': [0, 1, 2],
        'marker': {
            'size': 1.5,
            'color': [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            'opacity': 1
        }
    }

    # Mock PreprocessService.get_ply
    with patch('app.services.preprocess_service.PreprocessService.get_ply', return_value=mock_ply_data) as mock_get_ply:
        response = client.get(f'/api/preprocess/{param}/{ply_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [mock_ply_data]
    mock_get_ply.assert_called_once_with(ply_id, param)

def test_get_preprocess_process_ply_not_found(client, mongo):
    """
    Test the /api/preprocess/<param>/<ply_id> endpoint when PLY is not found.
    """
    param = "filtered_ply"
    ply_id = str(ObjectId())  # Non-existent ID

    # Mock PreprocessService.get_ply to return None
    with patch('app.services.preprocess_service.PreprocessService.get_ply', return_value=None) as mock_get_ply:
        response = client.get(f'/api/preprocess/{param}/{ply_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": f"{param} ply not found"}
    mock_get_ply.assert_called_once_with(ply_id, param)