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
        # 'MONGODB_URI': 'mongodb://localhost:27017/dromo_test'
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
    assert b"Welcome to the DROMO API" in response.data

def test_upload_visual_data_success(client, mongo):
    """
    Scenario: Successfully upload visual data
        Given I have a video file
        When I upload the file with a title
        Then I should receive a success message
        And the file should be stored in the database
    """
    data = {
        'title': 'Test Video',
        'file': (BytesIO(b'fake video content'), 'test_video.mp4')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200

    response_data = json.loads(response.data.decode('utf-8'))
    assert "message" in response_data
    assert "video_id" in response_data
    assert response_data["message"] == "Upload success"

    # Check if the video was stored in MongoDB
    video = mongo.videos.find_one({'_id': ObjectId(response_data['video_id'])})
    assert video is not None
    assert video['title'] == 'Test Video'
    assert 'file_path' in video

def test_upload_visual_data_no_file(client):
    """
    Scenario: Attempt to upload without a file
        Given I don't include a file in my upload
        When I try to upload
        Then I should receive an error message
    """
    data = {'title': 'Test Video'}
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
        'title': 'Test Video',
        'file': (BytesIO(b'fake video content'), '')
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

def test_video_retrieval(client, mongo):
    """
    Scenario: Retrieve uploaded video information
        Given I have uploaded a video
        When I request information about the video
        Then I should receive the correct video details
    """
    # First, upload a video
    upload_data = {
        'title': 'Retrieval Test Video',
        'file': (BytesIO(b'fake video content for retrieval'), 'retrieval_test.mp4')
    }
    upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
    upload_result = json.loads(upload_response.data.decode('utf-8'))
    video_id = upload_result['video_id']

    # Now, retrieve the video information
    response = client.get(f'/api/videos/{video_id}')
    assert response.status_code == 200

    video_data = json.loads(response.data.decode('utf-8'))
    assert video_data['title'] == 'Retrieval Test Video'
    assert 'file_path' in video_data
    assert 'timestamp' in video_data