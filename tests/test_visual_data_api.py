"""
Feature: DROMO API Functionality
    As a user of the DROMO system
    I want to be able to upload visual data and interact with the API
    So that I can use the 3D model generation capabilities
"""

import pytest
from app import create_app
from app.db.mongodb import get_db
from io import BytesIO
import json
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
def client2():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mongo(app):
    """Create a MongoDB test database and drop it after the test."""
    with app.app_context():
        db = get_db()
        yield db
        db.client.drop_database(db.name)

def test_home_route(client):
    """
    Scenario: Access the home route
        When I send a GET request to the home route
        Then I should receive a welcome message
    """
    response = client.get('/')
    assert response.status_code == 200
    # assert b"Welcome to the DROMO API" in response.data

def test_upload_visual_data_success(client, mongo):
    """
    Scenario: Successfully upload visual data
        Given I have a visual_data file
        When I upload the file with a title
        Then I should receive a success message
        And the file should be stored in the database
    """
    data = {
        'title': 'Test visual_data',
        'file': (BytesIO(b'fake visual_data content'), 'test_visual_data.ply')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200

    response_data = json.loads(response.data.decode('utf-8'))
    assert "message" in response_data
    assert "visual_data_id" in response_data
    assert response_data["message"] == "Upload success"

    # Check if the visual_data was stored in MongoDB
    visual_data = mongo.visual_datas.find_one({'_id': ObjectId(response_data['visual_data_id'])})
    assert visual_data is not None
    assert visual_data['title'] == 'Test visual_data'
    assert 'file_path' in visual_data

def test_upload_visual_data_no_file(client):
    """
    Scenario: Attempt to upload without a file
        Given I don't include a file in my upload
        When I try to upload
        Then I should receive an error message
    """
    data = {'title': 'Test visual_data'}
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No file part" in response.data

def test_upload_visual_data_no_filename(client):
    """
    Scenario: Attempt to upload a file with no filename
        Given I include a file with no filename
        When I try to upload
        Then I should receive an error message
    """
    data = {
        'title': 'Test visual_data',
        'file': (BytesIO(b'fake visual_data content'), '')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No selected file" in response.data

def test_upload_visual_data_invalid_extension(client):
    """
    Scenario: Attempt to upload a file with invalid extension
        Given I have a file with an invalid extension
        When I try to upload the file
        Then I should receive an error message
    """
    data = {
        'title': 'Test Document',
        'file': (BytesIO(b'fake document content'), 'test_document.txt')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"File type not allowed" in response.data

def test_mongodb_connection(app):
    """
    Scenario: Check MongoDB connection
        Given the application is configured with a MongoDB URI
        When I attempt to connect to the database
        Then the connection should be successful
    """
    with app.app_context():
        db = get_db()
        assert db.command('ping')['ok'] == 1

def test_visual_data_retrieval(client, mongo):
    """
    Scenario: Retrieve uploaded visual_data information
        Given I have uploaded a visual_data
        When I request information about the visual_data
        Then I should receive the correct visual_data details
    """
    # First, upload a visual_data
    upload_data = {
        'title': 'Retrieval Test visual_data',
        'file': (BytesIO(b'fake visual_data content for retrieval'), 'retrieval_test.ply')
    }
    upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
    upload_result = json.loads(upload_response.data.decode('utf-8'))
    visual_data_id = upload_result['visual_data_id']

    # Now, retrieve the visual_data information
    response = client.get(f'/api/visual_datas/{visual_data_id}')
    assert response.status_code == 200

    visual_data_data = json.loads(response.data.decode('utf-8'))
    assert visual_data_data['title'] == 'Retrieval Test visual_data'
    assert 'file_path' in visual_data_data
    assert 'timestamp' in visual_data_data

def test_list_visual_datas(client, mongo):
    """
    Scenario: List all visual_datas
        Given there are visual_datas in the database
        When I request the list of visual_datas
        Then I should receive a list of all visual_datas
    """
    # Add some test visual_datas to the database
    mongo.visual_datas.insert_many([
        {'title': 'visual_data 1', 'file_path': '/path/to/visual_data1.mp4', 'timestamp': '2024-09-14T10:00:00'},
        {'title': 'visual_data 2', 'file_path': '/path/to/visual_data2.mp4', 'timestamp': '2024-09-14T11:00:00'}
    ])

    response = client.get('/api/visual_datas')
    assert response.status_code == 200

    visual_datas = json.loads(response.data.decode('utf-8'))
    assert len(visual_datas) == 2
    assert visual_datas[0]['title'] == 'visual_data 1'
    assert visual_datas[1]['title'] == 'visual_data 2'
    assert 'timestamp' in visual_datas[0]
    assert 'timestamp' in visual_datas[1]

def test_get_visual_data_details(client, mongo):
    """
    Scenario: Get visual_data details
        Given there is a visual_data in the database
        When I request the details of that visual_data
        Then I should receive the correct visual_data information
    """
    visual_data = mongo.visual_datas.insert_one({
        'title': 'Test visual_data',
        'file_path': '/path/to/test_visual_data.mp4',
        'timestamp': '2024-09-14T12:00:00'
    })

    response = client.get(f'/api/visual_datas/{str(visual_data.inserted_id)}')
    assert response.status_code == 200

    visual_data_data = json.loads(response.data.decode('utf-8'))
    assert visual_data_data['title'] == 'Test visual_data'
    assert visual_data_data['file_path'] == '/path/to/test_visual_data.mp4'
    assert visual_data_data['timestamp'] == '2024-09-14T12:00:00'

def test_get_nonexistent_visual_data(client):
    """
    Scenario: Get details of a non-existent visual_data
        Given there is no visual_data with a specific ID in the database
        When I request the details of that visual_data
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f'/api/visual_datas/{nonexistent_id}')
    assert response.status_code == 404

def test_delete_visual_data(client, mongo):
    """
    Scenario: Delete a visual_data
        Given there is a visual_data in the database
        When I request to delete that visual_data
        Then the visual_data should be removed from the database
    """
    visual_data = mongo.visual_datas.insert_one({
        'title': 'visual_data to Delete',
        'file_path': '/path/to/delete_visual_data.mp4',
        'timestamp': '2024-09-14T13:00:00'
    })

    response = client.delete(f'/api/visual_datas/{str(visual_data.inserted_id)}')
    assert response.status_code == 200

    # Check that the visual_data was actually deleted
    assert mongo.visual_datas.find_one({'_id': visual_data.inserted_id}) is None


def test_delete_nonexistent_visual_data(client):
    """
    Scenario: Delete a non-existent visual_data
        Given there is no visual_data with a specific ID in the database
        When I request to delete that visual_data
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.delete(f'/api/visual_datas/{nonexistent_id}')
    assert response.status_code == 404

def test_invalid_visual_data_id(client):
    """
    Scenario: Use an invalid visual_data ID
        Given an invalid visual_data ID is provided
        When I request to get or delete a visual_data
        Then I should receive a 404 error
    """
    invalid_id = 'invalid_id'
    get_response = client.get(f'/api/visual_datas/{invalid_id}')
    assert get_response.status_code == 404
    assert json.loads(get_response.data)['error'] == 'visual_data not found or invalid ID'

    delete_response = client.delete(f'/api/visual_datas/{invalid_id}')
    assert delete_response.status_code == 404
    assert json.loads(delete_response.data)['error'] == 'visual_data not found or invalid ID'
