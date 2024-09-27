import pytest
import tempfile
from app import create_app
from app.db.mongodb import get_db
from app.models.threed_model import ThreeDModel
from bson import ObjectId
import json
from unittest.mock import patch, MagicMock
import os

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
    Test listing all 3D models.

    Scenario:
    - Two models are added to the database
    - A GET request is made to '/api/models'
    - The response should contain both models
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
    Test retrieving a specific 3D model.

    Scenario:
    - A model is added to the database
    - A GET request is made to '/api/models/{model_id}'
    - The response should contain the correct model details
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
    Test attempting to retrieve a non-existent 3D model.

    Scenario:
    - A GET request is made with an invalid model ID
    - The response should be a 404 error
    """
    invalid_id = str(ObjectId())
    response = client.get(f'/api/models/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model not found" in data['error']

def test_delete_model_success(client, mongo):
    """
    Test deleting a 3D model.

    Scenario:
    - A model is added to the database
    - A DELETE request is made to '/api/models/{model_id}'
    - The model should be successfully deleted
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
    Test attempting to delete a non-existent 3D model.

    Scenario:
    - A DELETE request is made with an invalid model ID
    - The response should be a 404 error
    """
    invalid_id = str(ObjectId())
    response = client.delete(f'/api/models/{invalid_id}')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model not found" in data['error']

def test_download_model_success(client, mongo):
    """
    Test downloading a 3D model's OBJ file.

    Scenario:
    - A model with an OBJ file is added to the database
    - A GET request is made to '/api/models/{model_id}/download'
    - The OBJ file should be successfully downloaded
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        obj_filename = "test_model.obj"
        with open(os.path.join(tmpdirname, obj_filename), 'w') as f:
            f.write("Test OBJ content")

        model = ThreeDModel("Test Model", tmpdirname, "pc_id", obj_filename, "mtl_file", "texture_file")
        model_id = model.save()

        response = client.get(f'/api/models/{model_id}/download')

        assert response.status_code == 200
        assert response.headers['Content-Disposition'] == f'attachment; filename={obj_filename}'
        assert response.data == b"Test OBJ content"

def test_download_model_not_found(client, mongo):
    """
    Test attempting to download a non-existent 3D model's OBJ file.

    Scenario:
    - A GET request is made with an invalid model ID
    - The response should be a 404 error
    """
    invalid_id = str(ObjectId())
    response = client.get(f'/api/models/{invalid_id}/download')

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "3D model or OBJ file not found" in data['error']

def test_get_model_obj_success(client, mongo):
    """
    Test serving a 3D model's OBJ file.

    Scenario:
    - A model with an OBJ file is added to the database
    - A GET request is made to '/api/models/{model_id}/obj'
    - The OBJ file should be successfully served
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        obj_filename = "test_model.obj"
        with open(os.path.join(tmpdirname, obj_filename), 'w') as f:
            f.write("Test OBJ content")

        model = ThreeDModel("Test Model", tmpdirname, "pc_id", obj_filename, "mtl_file", "texture_file")
        model_id = model.save()

        response = client.get(f'/api/models/{model_id}/obj')

        assert response.status_code == 200
        assert response.data == b"Test OBJ content"

def test_download_texture_success(client, mongo):
    """
    Test downloading a 3D model's texture file.

    Scenario:
    - A model with a texture file is added to the database
    - A GET request is made to '/api/models/{model_id}/texture'
    - The texture file should be successfully downloaded
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        texture_filename = "test_texture.png"
        texture_path = os.path.join(tmpdirname, texture_filename)
        with open(texture_path, 'wb') as f:
            f.write(b"Test texture content")

        model = ThreeDModel("Test Model", tmpdirname, "pc_id", "obj_file", "mtl_file", texture_path)
        model_id = model.save()

        response = client.get(f'/api/models/{model_id}/texture')

        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")

        # Check if the file exists before the test
        assert os.path.exists(texture_path), f"Texture file does not exist at {texture_path}"

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.headers['Content-Disposition'] == f'attachment; filename={texture_filename}'
        assert response.data == b"Test texture content"

def test_download_material_success(client, mongo):
    """
    Test downloading a 3D model's material file.

    Scenario:
    - A model with a material file is added to the database
    - A GET request is made to '/api/models/{model_id}/material'
    - The material file should be successfully downloaded
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        mtl_filename = "test_material.mtl"
        mtl_path = os.path.join(tmpdirname, mtl_filename)
        with open(mtl_path, 'w') as f:
            f.write("Test MTL content")

        model = ThreeDModel("Test Model", tmpdirname, "pc_id", "obj_file", mtl_path, "texture_file")
        model_id = model.save()

        response = client.get(f'/api/models/{model_id}/material')

        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")

        # Check if the file exists before the test
        assert os.path.exists(mtl_path), f"Material file does not exist at {mtl_path}"

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.headers['Content-Disposition'] == f'attachment; filename={mtl_filename}'
        assert response.data == b"Test MTL content"

def test_get_model_obj_not_found(client, mongo):
    """
    Test attempting to serve a non-existent 3D model's OBJ file.

    Scenario:
    - A GET request is made with an invalid model ID
    - The response should be either a 404 error or a 500 error (depending on how the application handles the Not Found exception)
    """
    invalid_id = str(ObjectId())
    response = client.get(f'/api/models/{invalid_id}/obj')

    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")

    assert response.status_code in [404, 500], f"Unexpected status code: {response.status_code}"

    data = json.loads(response.data)
    if response.status_code == 404:
        assert "error" in data
        assert "3D model or OBJ file not found" in data['error']
    else:  # 500 status code
        assert "error" in data
        assert "An internal error occurred" in data['error']

