import pytest
from app import create_app
from app.db.mongodb import get_db
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


def test_preprocess_video_success(client, mongo):
    """
    Scenario: Successfully preprocess a video
        Given I have a video in the database
        When I send a POST request to preprocess the video
        Then I should receive the processed video data
    """
    # First, upload a ply
    with open('tests/ply/input.ply', 'rb') as video_file:
        upload_data = {
            'title': 'Test ply',
            'file': (video_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        video_id = upload_result['Video_id']
        assert video_id
        print("#video_id", video_id)

    # Now, preprocess the video
    preprocess_response = client.post(f'/api/preprocess/{video_id}')
    assert preprocess_response.status_code == 200

    preprocess_data = json.loads(preprocess_response.data.decode('utf-8'))
    assert preprocess_data['ply_id'] == video_id
    assert 'frames_processed' in preprocess_data
    assert 'frames_directory' in preprocess_data



def test_preprocess_video_not_found(client):
    """
    Scenario: Preprocess a non-existent video
        Given a video ID that does not exist
        When I send a POST request to preprocess the video
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.post(f'/api/preprocess/{nonexistent_id}')
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'Video not found or invalid ID'

def test_progress_process_video_success(client, mongo):
    """
    Scenario: Retrieve progress of video processing
        Given a video is being processed
        When I request the processing progress
        Then I should receive the progress data
    """
    # First, upload a ply
    with open('tests/ply/input.ply', 'rb') as video_file:
        upload_data = {
            'title': 'Test Video',
            'file': (video_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        video_id = upload_result['video_id']
        assert video_id
        print("#video_id", video_id)

    # Process the video to simulate progress
    client.post(f'/api/preprocess/{video_id}')

    # Now, get the processing progress
    progress_response = client.get(f'/api/preprocess/progress/{video_id}')
    assert progress_response.status_code == 200

    progress_data = json.loads(progress_response.data.decode('utf-8'))
    assert progress_data['ply_id'] == video_id
    assert 'point_cloud_id' in progress_data
    assert 'processed' in progress_data

def test_progress_process_video_not_found(client):
    """
    Scenario: Retrieve progress of a non-existent video
        Given a video ID that does not exist
        When I request the processing progress
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f'/api/preprocess/progress/{nonexistent_id}')
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'Video not found or invalid ID'


def test_preprocess_video_success(client, mongo):
    """
    Scenario: Successfully preprocess a video
        Given I have a video in the database
        When I send a POST request to preprocess the video
        Then I should receive the processed video data
    """
    # First, upload a video
    with open('tests/ply/input.ply', 'rb') as video_file:
        upload_data = {
            'title': 'Test Video',
            'file': (video_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        video_id = upload_result['video_id']
        assert video_id
        print("#video_id", video_id)

    # Now, preprocess the video
    preprocess_response = client.post(f'/api/preprocess/{video_id}')
    assert preprocess_response.status_code == 200

    preprocess_data = json.loads(preprocess_response.data.decode('utf-8'))
    assert preprocess_data['ply_id'] == video_id
    assert 'point_cloud_id' in preprocess_data
    assert 'processed' in preprocess_data
