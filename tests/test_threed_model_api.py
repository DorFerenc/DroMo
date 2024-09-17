import pytest
import tempfile
from app import create_app
from app.db.mongodb import get_db
from app.models.threed_model import ThreeDModel
from bson import ObjectId
import json
from unittest.mock import patch, MagicMock

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

def test_list_models_success(client, mongo):
    """
    Scenario: Successfully list all 3D models
    """
    model1 = ThreeDModel("Model 1", "folder1", "pc_id_1", "obj_1", "mtl_1", "texture_1")
    model2 = ThreeDModel("Model 2", "folder2", "pc_id_2", "obj_2", "mtl_2", "texture_2")
    model1.save()
    model2.save()

    response = client.get('/api/models')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == "Model 1"
    assert data[1]['name'] == "Model 2"

def test_get_model_success(client, mongo):
    """
    Scenario: Successfully get a specific 3D model
    """
    model = ThreeDModel("Test Model", "test_folder", "pc_id", "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.get(f'/api/models/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == "Test Model"
    assert data['point_cloud_id'] == "pc_id"
    assert data['folder_path'] == "test_folder"

def test_get_model_not_found(client, mongo):
    """
    Scenario: Attempt to get a non-existent 3D model
    """
    invalid_id = str(ObjectId())
    response = client.get(f'/api/models/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model not found" in data['error']

def test_delete_model_success(client, mongo):
    """
    Scenario: Successfully delete a 3D model
    """
    model = ThreeDModel("Test Model", "test_folder", "pc_id", "obj_file", "mtl_file", "texture_file")
    model_id = model.save()

    response = client.delete(f'/api/models/{model_id}')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "3D model deleted successfully" in data['message']

    # Verify the model is no longer in the database
    assert ThreeDModel.get_by_id(model_id) is None

def test_delete_model_not_found(client, mongo):
    """
    Scenario: Attempt to delete a non-existent 3D model
    """
    invalid_id = str(ObjectId())
    response = client.delete(f'/api/models/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model not found" in data['error']

# def test_download_model_success(client, mongo):
#     """
#     Scenario: Successfully download a 3D model's OBJ file
#     """
#     # Create a temporary directory and file for testing
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         obj_filename = "test_model.obj"
#         with open(os.path.join(tmpdirname, obj_filename), 'w') as f:
#             f.write("Test OBJ content")

#         model = ThreeDModel("Test Model", tmpdirname, "pc_id", obj_filename, "mtl_file", "texture_file")
#         model_id = model.save()

#         response = client.get(f'/api/models/{model_id}/download')

#         print(f"Response status: {response.status_code}")
#         print(f"Response data: {response.data}")

#         assert response.status_code == 200
#         assert response.headers['Content-Disposition'] == f'attachment; filename={obj_filename}'
#         assert response.data == b"Test OBJ content"


def test_download_model_not_found(client, mongo):
    """
    Scenario: Attempt to download a non-existent 3D model's OBJ file
    """
    invalid_id = str(ObjectId())
    response = client.get(f'/api/models/{invalid_id}/download')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model or OBJ file not found" in data['error']

# You can add similar tests for downloading texture and material files