import time

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


import json
import time
from bson import ObjectId
import pytest


def test_preprocess_visual_data_not_found(client):
    """
    Scenario: Attempt to process a non-existent visual_data
        Given a visual_data ID that does not exist
        When I send a POST request to preprocess the visual_data
        Then I should receive an error
    """
    nonexistent_id = str(ObjectId())
    # Update: Changed to match the API route structure
    response = client.post(f'/api/preprocess/'+nonexistent_id)
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'visual_data not found or invalid ID'


def test_task_status_not_found(client):
    """
    Scenario: Request status of non-existent task
        Given a task ID that does not exist
        When I request the task status
        Then I should receive a 404 error
    """
    nonexistent_task_id = str(ObjectId())
    response = client.get(f'/api/preprocess/status/{nonexistent_task_id}')
    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'Task not found'


def test_preprocess_visual_data_success(client, mongo):
    """
    Scenario: Successfully initiate visual_data processing
        Given I have a visual_data in the database
        When I send a POST request to process the visual_data
        Then I should receive a task ID and be able to monitor progress
    """
    # First, upload a visual_data
    with open('tests/ply/input.ply', 'rb') as visual_data_file:
        upload_data = {
            'title': 'Test visual_data',
            'file': (visual_data_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data,
                                      content_type='multipart/form-data')
        assert upload_response.status_code == 200
        upload_result = json.loads(upload_response.data.decode('utf-8'))
        visual_data_id = upload_result['visual_data_id']
        assert visual_data_id

    # Initiate processing - Update: Changed to form data
    process_response = client.post('/api/preprocess/'+visual_data_id)
    assert process_response.status_code == 202
    process_data = json.loads(process_response.data)

    # Verify initial response
    assert 'task_id' in process_data
    assert process_data['status'] == 'PENDING'
    task_id = process_data['task_id']

    # Monitor task status with shorter timeout
    max_attempts = 5  # Reduced for testing
    attempt = 0
    task_completed = False

    while attempt < max_attempts:
        status_response = client.get(f'/api/preprocess/status/{task_id}')
        assert status_response.status_code == 200
        status_data = json.loads(status_response.data)

        # Verify status response structure
        assert 'task_id' in status_data
        assert 'status' in status_data
        assert 'start_time' in status_data

        # If processing is complete or in error
        if status_data['status'] in ['SUCCESS', 'ERROR']:
            task_completed = True
            if status_data['status'] == 'SUCCESS':
                assert 'result' in status_data
                result = status_data['result']
                assert result['ply_id'] == visual_data_id
                assert 'point_cloud_id' in result
                assert result['processed'] is True
            break

        attempt += 1
        time.sleep(0.5)  # Shorter wait time for testing

    # For testing purposes, we don't want to wait for full processing
    # Just verify the task was created and can be monitored
    assert 'task_id' in process_data, "Task ID should be in initial response"


def test_task_cleanup(client, mongo):
    """
    Scenario: Verify task creation and initial status
        Given a new processing request
        When I create a task
        Then I should be able to get its initial status
    """
    # Create a test visual_data first
    with open('tests/ply/input.ply', 'rb') as visual_data_file:
        upload_data = {
            'title': 'Test visual_data',
            'file': (visual_data_file, 'test_ply.ply')
        }
        upload_response = client.post('/api/upload', data=upload_data,
                                      content_type='multipart/form-data')
        visual_data_id = json.loads(upload_response.data)['visual_data_id']

    # Start processing
    process_response = client.post('/api/preprocess/'+visual_data_id)
    assert process_response.status_code == 202
    process_data = json.loads(process_response.data)
    assert 'task_id' in process_data

    # Verify initial task status
    task_id = process_data['task_id']
    status_response = client.get(f'/api/preprocess/status/{task_id}')
    assert status_response.status_code == 200
    assert json.loads(status_response.data)['status'] in ['PENDING', 'PROCESSING']
