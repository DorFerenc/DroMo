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


def test_preprocess_visual_data_success(client, mongo):
    """
    Scenario: Successfully preprocess a visual_data
        Given I have a visual_data in the database
        When I send a POST request to preprocess the visual_data
        Then I should receive the processed visual_data data
    """
    # First, upload a ply
    with open('tests/ply/input.ply', 'rb') as visual_data_file:
        upload_data = {
            'title': 'Test ply',
            'file': (visual_data_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        visual_data_id = upload_result['visual_data_id']
        assert visual_data_id
        print("#visual_data_id", visual_data_id)

    # Now, preprocess the visual_data
    preprocess_response = client.post(f'/api/preprocess/{visual_data_id}')
    assert preprocess_response.status_code == 200

    preprocess_data = json.loads(preprocess_response.data.decode('utf-8'))
    assert preprocess_data['ply_id'] == visual_data_id
    assert 'frames_processed' in preprocess_data
    assert 'frames_directory' in preprocess_data



def test_preprocess_visual_data_not_found(client):
    """
    Scenario: Preprocess a non-existent visual_data
        Given a visual_data ID that does not exist
        When I send a POST request to preprocess the visual_data
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.post(f'/api/preprocess/{nonexistent_id}')
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'visual_data not found or invalid ID'

def test_progress_process_visual_data_success(client, mongo):
    """
    Scenario: Retrieve progress of visual_data processing
        Given a visual_data is being processed
        When I request the processing progress
        Then I should receive the progress data
    """
    # First, upload a ply
    with open('tests/ply/input.ply', 'rb') as visual_data_file:
        upload_data = {
            'title': 'Test visual_data',
            'file': (visual_data_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        visual_data_id = upload_result['visual_data_id']
        assert visual_data_id
        print("#visual_data_id", visual_data_id)

    # Process the visual_data to simulate progress
    client.post(f'/api/preprocess/{visual_data_id}')

    # Now, get the processing progress
    progress_response = client.get(f'/api/preprocess/progress/{visual_data_id}')
    assert progress_response.status_code == 200

    progress_data = json.loads(progress_response.data.decode('utf-8'))
    assert progress_data['ply_id'] == visual_data_id
    assert 'point_cloud_id' in progress_data
    assert 'processed' in progress_data

def test_progress_process_visual_data_not_found(client):
    """
    Scenario: Retrieve progress of a non-existent visual_data
        Given a visual_data ID that does not exist
        When I request the processing progress
        Then I should receive a 404 error
    """
    nonexistent_id = str(ObjectId())
    response = client.get(f'/api/preprocess/progress/{nonexistent_id}')
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'visual_data not found or invalid ID'


def test_preprocess_visual_data_success(client, mongo):
    """
    Scenario: Successfully preprocess a visual_data
        Given I have a visual_data in the database
        When I send a POST request to preprocess the visual_data
        Then I should receive the processed visual_data data
    """
    # First, upload a visual_data
    with open('tests/ply/input.ply', 'rb') as visual_data_file:
        upload_data = {
            'title': 'Test visual_data',
            'file': (visual_data_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data, content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        visual_data_id = upload_result['visual_data_id']
        assert visual_data_id
        print("#visual_data_id", visual_data_id)

    # Now, preprocess the visual_data
    preprocess_response = client.post(f'/api/preprocess/{visual_data_id}')
    assert preprocess_response.status_code == 200

    preprocess_data = json.loads(preprocess_response.data.decode('utf-8'))
    assert preprocess_data['ply_id'] == visual_data_id
    assert 'point_cloud_id' in preprocess_data
    assert 'processed' in preprocess_data
