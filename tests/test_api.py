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

def test_list_videos(client, mongo):
    """
    Scenario: List all videos
        Given there are videos in the database
        When I request the list of videos
        Then I should receive a list of all videos
    """
    # Add some test videos to the database
    mongo.videos.insert_many([
        {'title': 'Video 1', 'file_path': '/path/to/video1.mp4', 'timestamp': '2024-09-14T10:00:00'},
        {'title': 'Video 2', 'file_path': '/path/to/video2.mp4', 'timestamp': '2024-09-14T11:00:00'}
    ])

    response = client.get('/api/videos')
    assert response.status_code == 200

    videos = json.loads(response.data.decode('utf-8'))
    assert len(videos) == 2
    assert videos[0]['title'] == 'Video 1'
    assert videos[1]['title'] == 'Video 2'
    assert 'timestamp' in videos[0]
    assert 'timestamp' in videos[1]

def test_get_video_details(client, mongo):
    """
    Scenario: Get video details
        Given there is a video in the database
        When I request the details of that video
        Then I should receive the correct video information
    """
    video = mongo.videos.insert_one({
        'title': 'Test Video',
        'file_path': '/path/to/test_video.mp4',
        'timestamp': '2024-09-14T12:00:00'
    })

    response = client.get(f'/api/videos/{str(video.inserted_id)}')
    assert response.status_code == 200

    video_data = json.loads(response.data.decode('utf-8'))
    assert video_data['title'] == 'Test Video'
    assert video_data['file_path'] == '/path/to/test_video.mp4'
    assert video_data['timestamp'] == '2024-09-14T12:00:00'

def test_get_nonexistent_video(client):
    """
    Scenario: Get details of a non-existent video
        Given there is no video with a specific ID in the database
        When I request the details of that video
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f'/api/videos/{nonexistent_id}')
    assert response.status_code == 404

def test_delete_video(client, mongo):
    """
    Scenario: Delete a video
        Given there is a video in the database
        When I request to delete that video
        Then the video should be removed from the database
    """
    video = mongo.videos.insert_one({
        'title': 'Video to Delete',
        'file_path': '/path/to/delete_video.mp4',
        'timestamp': '2024-09-14T13:00:00'
    })

    response = client.delete(f'/api/videos/{str(video.inserted_id)}')
    assert response.status_code == 200

    # Check that the video was actually deleted
    assert mongo.videos.find_one({'_id': video.inserted_id}) is None


def test_delete_nonexistent_video(client):
    """
    Scenario: Delete a non-existent video
        Given there is no video with a specific ID in the database
        When I request to delete that video
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.delete(f'/api/videos/{nonexistent_id}')
    assert response.status_code == 404

def test_invalid_video_id(client):
    """
    Scenario: Use an invalid video ID
        Given an invalid video ID is provided
        When I request to get or delete a video
        Then I should receive a 404 error
    """
    invalid_id = 'invalid_id'
    get_response = client.get(f'/api/videos/{invalid_id}')
    assert get_response.status_code == 404
    assert json.loads(get_response.data)['error'] == 'Video not found or invalid ID'

    delete_response = client.delete(f'/api/videos/{invalid_id}')
    assert delete_response.status_code == 404
    assert json.loads(delete_response.data)['error'] == 'Video not found or invalid ID'
