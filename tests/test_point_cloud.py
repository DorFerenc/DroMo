import pytest
from app import create_app
from app.db.mongodb import get_db
from app.models.point_cloud import PointCloud
from io import BytesIO
import json
from bson import ObjectId, errors as bson_errors
import numpy as np

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

def test_point_cloud_model():
    """
    Scenario: Create and manipulate a PointCloud object
        Given I have point cloud data
        When I create a PointCloud object
        Then it should correctly store and represent the data
    """
    points = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    colors = np.array([[255, 0, 0], [0, 255, 0]])
    pc = PointCloud("Test Cloud", points, colors)

    assert pc.name == "Test Cloud"
    assert len(pc.points) == 2
    assert len(pc.colors) == 2
    assert pc.colors is not None
    assert isinstance(pc.points, np.ndarray)
    assert isinstance(pc.colors, np.ndarray)

def test_point_cloud_from_string():
    """
    Scenario: Create a PointCloud object from a string
        Given I have point cloud data as a string
        When I create a PointCloud object using from_string method
        Then it should correctly parse and store the data
    """
    pc_string = """x,y,z,r,g,b
0.1,0.2,0.3,255,0,0
0.4,0.5,0.6,0,255,0"""
    pc = PointCloud.from_string("Test Cloud", pc_string)

    assert pc.name == "Test Cloud"
    assert len(pc.points) == 2
    assert len(pc.colors) == 2
    assert pc.colors is not None
    assert isinstance(pc.points, np.ndarray)
    assert isinstance(pc.colors, np.ndarray)

def test_upload_point_cloud(client, mongo):
    """
    Scenario: Upload a point cloud
        Given I have point cloud data
        When I upload it through the API
        Then it should be stored in the database and return a success message
    """
    pc_string = """x,y,z,r,g,b
0.1,0.2,0.3,255,0,0
0.4,0.5,0.6,0,255,0"""

    data = {
        'name': 'Test Point Cloud',
        'file': (BytesIO(pc_string.encode()), 'test_cloud.txt')
    }
    response = client.post('/api/point_clouds', data=data, content_type='multipart/form-data')
    assert response.status_code == 200

    response_data = json.loads(response.data.decode('utf-8'))
    assert "message" in response_data
    assert "point_cloud_id" in response_data
    assert response_data["message"] == "Point cloud uploaded successfully"

    # Check if the point cloud was stored in MongoDB
    pc = mongo.point_clouds.find_one({'_id': ObjectId(response_data['point_cloud_id'])})
    assert pc is not None
    assert pc['name'] == 'Test Point Cloud'
    assert 'points' in pc
    assert 'colors' in pc

def test_get_point_cloud(client, mongo):
    """
    Scenario: Retrieve a point cloud
        Given there is a point cloud in the database
        When I request its details through the API
        Then I should receive the correct point cloud information
    """
    pc = PointCloud("Test Cloud", np.array([[0.1, 0.2, 0.3]]), np.array([[255, 0, 0]]))
    pc_id = pc.save()

    response = client.get(f'/api/point_clouds/{pc_id}')
    assert response.status_code == 200

    pc_data = json.loads(response.data.decode('utf-8'))
    assert pc_data['name'] == 'Test Cloud'
    assert pc_data['num_points'] == 1
    assert pc_data['has_colors'] == True

def test_list_point_clouds(client, mongo):
    """
    Scenario: List all point clouds
        Given there are point clouds in the database
        When I request the list of point clouds
        Then I should receive a list of all point clouds
    """
    PointCloud("Cloud 1", np.array([[0.1, 0.2, 0.3]])).save()
    PointCloud("Cloud 2", np.array([[0.4, 0.5, 0.6]])).save()

    response = client.get('/api/point_clouds')
    assert response.status_code == 200

    point_clouds = json.loads(response.data.decode('utf-8'))
    assert len(point_clouds) == 2
    assert point_clouds[0]['name'] == 'Cloud 1'
    assert point_clouds[1]['name'] == 'Cloud 2'

def test_delete_point_cloud(client, mongo):
    """
    Scenario: Delete a point cloud
        Given there is a point cloud in the database
        When I request to delete it through the API
        Then it should be removed from the database
    """
    pc = PointCloud("Cloud to Delete", np.array([[0.1, 0.2, 0.3]]))
    pc_id = pc.save()

    response = client.delete(f'/api/point_clouds/{pc_id}')
    assert response.status_code == 200

    # Check that the point cloud was actually deleted
    assert mongo.point_clouds.find_one({'_id': ObjectId(pc_id)}) is None

def test_get_nonexistent_point_cloud(client):
    """
    Scenario: Get details of a non-existent point cloud
        Given there is no point cloud with a specific ID in the database
        When I request the details of that point cloud
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f'/api/point_clouds/{nonexistent_id}')
    assert response.status_code == 404

def test_delete_nonexistent_point_cloud(client):
    """
    Scenario: Delete a non-existent point cloud
        Given there is no point cloud with a specific ID in the database
        When I request to delete that point cloud
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.delete(f'/api/point_clouds/{nonexistent_id}')
    assert response.status_code == 404

def test_invalid_point_cloud_id(client):
    """
    Scenario: Use an invalid point cloud ID
        Given an invalid point cloud ID is provided
        When I request to get or delete a point cloud
        Then I should receive a 400 error for invalid ID format
    """
    invalid_id = 'invalid_id'
    get_response = client.get(f'/api/point_clouds/{invalid_id}')
    assert get_response.status_code == 400
    assert json.loads(get_response.data)['error'] == 'Invalid point cloud ID'

    delete_response = client.delete(f'/api/point_clouds/{invalid_id}')
    assert delete_response.status_code == 400
    assert json.loads(delete_response.data)['error'] == 'Invalid point cloud ID'

def test_upload_large_point_cloud(client):
    """
    Scenario: Upload a large point cloud
    """
    large_pc_string = "x,y,z,r,g,b\n" + "\n".join([f"{i},{i},{i},255,0,0" for i in range(100000)])
    data = {
        'name': 'Large Point Cloud',
        'file': (BytesIO(large_pc_string.encode()), 'large_cloud.txt')
    }
    response = client.post('/api/point_clouds', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert "point_cloud_id" in response_data
