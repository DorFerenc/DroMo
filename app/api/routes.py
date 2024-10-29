"""API routes for the DROMO system."""
import logging
import uuid
from datetime import datetime
from threading import Thread

from flask import Blueprint, request, jsonify, current_app, send_file, abort, Response
from werkzeug.utils import secure_filename
from app.db.mongodb import get_db
from bson import ObjectId, errors as bson_errors
import os
import traceback
from typing import Dict, Any

from app.services.visual_data_service import VisualDataService
from app.services.reconstruction_service import ReconstructionService
from app.services.preprocess_service import PreprocessService
from app.services.recon_proc_visualization_service import ReconProcVisualizationService
from app.models.point_cloud import PointCloud
from app.models.threed_model import ThreeDModel
from app.api.task_manager import TaskManager

api_bp = Blueprint('api', __name__)

# Dependency Injection
visual_data_service = VisualDataService()
preprocess_service = PreprocessService()
reconstruction_service = ReconstructionService()
visualization_service = ReconProcVisualizationService()
# Helper functions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def create_error_response(message: str, status_code: int) -> tuple:
    """Create a standardized error response."""
    return jsonify({"error": message}), status_code

def create_success_response(data: Dict[str, Any], message: str = "Success") -> tuple:
    """Create a standardized success response."""
    response = {"message": message, "data": data}
    return jsonify(response), 200

@api_bp.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler for the API."""
    current_app.logger.error(f"An error occurred: {str(e)}", exc_info=True)
    return jsonify({"error": "An internal error occurred"}), 500

def process_in_background(task_id: str, visual_data_id: str):
    try:
        TaskManager.update_task_status(task_id, 'PROCESSING')

        # Your existing processing logic here
        result = preprocess_service.process_ply(visual_data_id)

        TaskManager.update_task_status(task_id, 'SUCCESS', result=result)
    except Exception as e:
        TaskManager.update_task_status(task_id, 'ERROR', error=str(e))

##################################################
# Upload visual data API
##################################################

@api_bp.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_visual_data():
    """
    Handle the upload of visual data.

    Returns:
        JSON response with upload status and visual_data ID.
    """
    if request.method == 'OPTIONS':
        return '', 200

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    title = request.form.get('title', 'Untitled')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        visual_data_id = visual_data_service.create_visual_data(title, file_path)

        return jsonify({
            "message": "Upload success",
            "visual_data_id": visual_data_id
        }), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400


@api_bp.route('/api/visual_datas/<visual_data_id>', methods=['GET'])
def get_visual_data(visual_data_id):
    """Retrieve information about a specific visual_data."""
    visual_data = visual_data_service.get_visual_data(visual_data_id)
    if visual_data:
        return jsonify({
            'id': str(visual_data['_id']),
            'title': visual_data['title'],
            'file_path': visual_data['file_path'],
            'timestamp': visual_data['timestamp'] #.isoformat()
        }), 200
    else:
        return jsonify({'error': 'visual_data not found or invalid ID'}), 404


@api_bp.route('/api/visual_datas', methods=['GET'])
def list_visual_datas():
    """List all visual_datas."""
    visual_datas = visual_data_service.get_all_visual_datas()
    return jsonify([{
        'id': str(visual_data['_id']),
        'title': visual_data['title'],
        'timestamp': visual_data['timestamp'] # .isoformat()
    } for visual_data in visual_datas]), 200


@api_bp.route('/api/visual_datas/<visual_data_id>', methods=['DELETE'])
def delete_visual_data(visual_data_id):
    """Delete a specific visual_data."""
    result = visual_data_service.delete_visual_data(visual_data_id)
    if result:
        return jsonify({'message': 'visual_data deleted successfully'}), 200
    else:
        return jsonify({'error': 'visual_data not found or invalid ID'}), 404

########################################################################
# Pre Process api
########################################################################


@api_bp.route('/api/preprocess/<visual_data_id>', methods=['POST'])
def process_visual_data(visual_data_id):
    """
    Start asynchronous preprocessing of visual_data
    """

    ply_file = VisualDataService.get_visual_data(visual_data_id)

    if not ply_file:
        return jsonify({
        'id': visual_data_id,
        'status': 'NOT FOUND',
        'error': 'visual_data not found or invalid ID'
    }), 404

    # Create a new task
    task_id = TaskManager.create_task(visual_data_id)

    # Start processing in background
    thread = Thread(target=process_in_background, args=(task_id, visual_data_id))
    thread.daemon = True  # Thread will be terminated when main process exits
    thread.start()

    return jsonify({
        'task_id': task_id,
        'status': 'PENDING'
    }), 202


@api_bp.route('/api/preprocess/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    Get the status of a processing task
    """
    task = TaskManager.get_task_status(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    response = {
        'task_id': task_id,
        'status': task['status'],
        'start_time': task['start_time'].isoformat(),
        'end_time': task['end_time'].isoformat() if task['end_time'] else None
    }

    if task['status'] == 'SUCCESS':
        response['result'] = task['result']
    elif task['status'] == 'ERROR':
        response['error'] = task['error']

    return jsonify(response)


# Add task cleanup route (optional)
@api_bp.route('/api/preprocess/cleanup', methods=['POST'])
def cleanup_tasks():
    """
    Clean up completed tasks older than 24 hours
    """
    TaskManager.clean_old_tasks()
    return jsonify({'status': 'success'})

########################################################################
# Point cloud api
########################################################################

@api_bp.route('/api/point_clouds', methods=['POST'])
def upload_point_cloud():
    """
    Handle the upload of point cloud data.

    Expects:
        - A 'file' in the request files
        - A 'name' in the form data (optional)

    Returns:
        JSON response with upload status and point cloud ID.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    name = request.form.get('name', 'Untitled Point Cloud')

    try:
        pc_data = file.read().decode('utf-8')
        pc = PointCloud.from_string(name, pc_data)
        pc_id = pc.save()
        return jsonify({
            "message": "Point cloud uploaded successfully",
            "point_cloud_id": pc_id
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/api/point_clouds/<point_cloud_id>', methods=['GET'])
def get_point_cloud(point_cloud_id: str):
    """Retrieve a specific point cloud."""
    try:
        ObjectId(point_cloud_id)  # Validate the ID format
    except bson_errors.InvalidId:
        return jsonify({'error': 'Invalid point cloud ID'}), 400

    pc = PointCloud.get_by_id(point_cloud_id)
    if pc:
        return jsonify({
            'id': point_cloud_id,
            'name': pc.name,
            'num_points': len(pc.points),
            'has_colors': pc.colors is not None,
            'timestamp': pc.timestamp.isoformat()
        }), 200
    else:
        return jsonify({'error': 'Point cloud not found'}), 404

@api_bp.route('/api/point_clouds', methods=['GET'])
def list_point_clouds():
    """List all point clouds."""
    point_clouds = PointCloud.list_all()
    return jsonify([{
        'id': str(pc['_id']),
        'name': pc['name'],
        'num_points': len(pc['points']),
        'has_colors': 'colors' in pc,
        'timestamp': pc['timestamp'].isoformat()
    } for pc in point_clouds]), 200

@api_bp.route('/api/point_clouds/<point_cloud_id>', methods=['DELETE'])
def delete_point_cloud(point_cloud_id):
    """Delete a specific point cloud."""
    db = get_db()
    try:
        preprocess_service.delete_ply_files(point_cloud_id)
        result = db.point_clouds.delete_one({'_id': ObjectId(point_cloud_id)})
        if result.deleted_count:
            return jsonify({'message': 'Point cloud deleted successfully'}), 200
        else:
            return jsonify({'error': 'Point cloud not found'}), 404
    except bson_errors.InvalidId:
        return jsonify({'error': 'Invalid point cloud ID'}), 400

@api_bp.route('/api/point_clouds/<point_cloud_id>/download', methods=['GET'])
def download_point_cloud(point_cloud_id):
    """Download the point cloud data as a CSV file."""
    try:
        current_app.logger.info(f"Attempting to download point cloud with ID: {point_cloud_id}")
        pc = PointCloud.get_by_id(point_cloud_id)
        if pc:
            current_app.logger.info(f"Point cloud found: {pc.name}")
            csv_data = pc.to_csv()
            current_app.logger.info(f"CSV data generated, size: {len(csv_data)} bytes")
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-disposition":
                         f"attachment; filename={pc.name}.csv"}
            )
        else:
            current_app.logger.warning(f"Point cloud not found for ID: {point_cloud_id}")
            return jsonify({'error': 'Point cloud not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error downloading point cloud: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Error downloading point cloud', 'details': str(e)}), 500

########################################################################
# Reconstruction
########################################################################


@api_bp.route('/api/reconstruct/<point_cloud_id>', methods=['POST'])
def reconstruct(point_cloud_id):
    """
    Start the reconstruction process for a given point cloud.

    Args:
        point_cloud_id (str): Point Cloud ID

    Returns:
        JSON response with reconstruction status and model ID.
    """
    try:
        model_id = reconstruction_service.start_reconstruction(point_cloud_id)

        return jsonify({
            "message": "Reconstruction completed successfully",
            "model_id": model_id
        }), 200

    except ValueError as e:
        current_app.logger.error(f"Reconstruction error: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Reconstruction error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/api/reconstruction_stages/<point_cloud_id>', methods=['GET'])
def get_reconstruction_stages(point_cloud_id):
    """
    Get the reconstruction stages for a given point cloud.

    Args:
        point_cloud_id: Point Cloud ID

    Returns:
        JSON response with reconstruction stages data.
    """
    current_app.logger.info(f"Received request for reconstruction stages of point cloud: {point_cloud_id}")
    try:
        stages = ReconstructionService.get_reconstruction_stages(point_cloud_id)
        current_app.logger.info(f"Successfully retrieved reconstruction stages for point cloud: {point_cloud_id}")
        return jsonify(stages), 200
    except ValueError as e:
        current_app.logger.error(f"Value error in reconstruction stages: {str(e)}")
        return jsonify({"error": str(e), "point_cloud_id": point_cloud_id}), 404
        # return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Unexpected error in reconstruction stages: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e), "point_cloud_id": point_cloud_id}), 500
        # return jsonify({"error": "Internal server error", "details": str(e)}), 500

########################################################################
# 3D Model API
########################################################################

@api_bp.route('/api/models', methods=['GET'])
def list_models():
    """List all 3D models."""
    models = ThreeDModel.get_all()
    return jsonify([{
        'id': str(model.id),
        'name': model.name,
        'folder_path': model.folder_path,
        'point_cloud_id': model.point_cloud_id,
        'obj_file': model.obj_file,
        'mtl_file': model.mtl_file,
        'texture_file': model.texture_file,
        'created_at': model.created_at.isoformat()
    } for model in models]), 200

@api_bp.route('/api/models/<model_id>', methods=['GET'])
def get_model(model_id):
    """Retrieve a specific 3D model."""
    model = ThreeDModel.get_by_id(model_id)
    if model:
        current_app.logger.info(f"GET -> Model found: {model.name}")
        return jsonify({
            'id': str(model.id),
            'name': model.name,
            'folder_path': model.folder_path,
            'point_cloud_id': model.point_cloud_id,
            'obj_file': model.obj_file,
            'mtl_file': model.mtl_file,
            'texture_file': model.texture_file,
            'created_at': model.created_at.isoformat()
        }), 200
    else:
        return jsonify({'error': '3D model not found'}), 404

@api_bp.route('/api/models/<model_id>', methods=['DELETE'])
def delete_model(model_id):
    """Delete a specific 3D model."""
    model = ThreeDModel.get_by_id(model_id)
    if model:
        # Delete associated files
        current_app.logger.info(f"DELETE -> Model found: {model.name}")
        for file_path in [model.obj_file, model.mtl_file, model.texture_file]:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        # Remove the model directory if it's empty
        if os.path.exists(model.folder_path) and not os.listdir(model.folder_path):
            os.rmdir(model.folder_path)

        # Delete the model from the database
        if ThreeDModel.delete(model_id):
            return jsonify({'message': '3D model deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete 3D model from database'}), 500
    else:
        return jsonify({'error': '3D model not found'}), 404

@api_bp.route('/api/models/<model_id>/download', methods=['GET'])
def download_model(model_id):
    """Download the OBJ file of a specific 3D model."""
    model = ThreeDModel.get_by_id(model_id)
    if model and model.obj_file:
        file_path = os.path.join(model.folder_path, model.obj_file)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'OBJ file not found on server'}), 404
    else:
        return jsonify({'error': '3D model or OBJ file not found'}), 404

@api_bp.route('/api/models/<model_id>/texture', methods=['GET'])
def download_texture(model_id):
    """Download the texture file of a specific 3D model."""
    current_app.logger.info(f"Attempting to download texture for model: {model_id}")
    model = ThreeDModel.get_by_id(model_id)
    if model and model.texture_file and os.path.exists(model.texture_file):
        current_app.logger.info(f"Texture found: {model.texture_file}")
        return send_file(model.texture_file, as_attachment=True)
    else:
        current_app.logger.error(f"Texture file not found for model: {model_id}")
        return jsonify({'error': '3D model or texture file not found'}), 404

@api_bp.route('/api/models/<model_id>/material', methods=['GET'])
def download_material(model_id):
    """Download the material (MTL) file of a specific 3D model."""
    current_app.logger.info(f"Attempting to download material for model: {model_id}")
    model = ThreeDModel.get_by_id(model_id)
    if model and model.mtl_file and os.path.exists(model.mtl_file):
        current_app.logger.info(f"Material found: {model.mtl_file}")
        return send_file(model.mtl_file, as_attachment=True)
    else:
        current_app.logger.error(f"Material file not found for model: {model_id}")
        return jsonify({'error': '3D model or material file not found'}), 404

@api_bp.route('/api/models/<model_id>/obj', methods=['GET'])
def get_model_obj(model_id):
    """Serve the OBJ file for a specific 3D model."""
    try:
        model = ThreeDModel.get_by_id(model_id)
        if model and model.obj_file:
            file_path = os.path.join(model.folder_path, model.obj_file)
            if os.path.exists(file_path):
                return send_file(file_path)
        return jsonify({"error": "3D model or OBJ file not found"}), 404
    except Exception as e:
        current_app.logger.error(f"An error occurred while serving OBJ file: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

########################################################################
# 3D Model with plotly API
########################################################################

@api_bp.route('/api/reconstruction/point_cloud/<model_id>')
def get_point_cloud_data(model_id):
    current_app.logger.info(f"Getting point cloud data for model: {model_id}")
    data = visualization_service.get_point_cloud_data(model_id)
    if data is None:
        return jsonify({"error": "Model or point cloud not found"}), 404
    return jsonify([data])

@api_bp.route('/api/reconstruction/initial_mesh/<model_id>')
def get_initial_mesh_data(model_id):
    try:
        current_app.logger.info(f"Getting initial mesh data for model: {model_id}")
        data = visualization_service.get_mesh_data(model_id, mesh_type='initial')
        if data is None:
            return jsonify({"error": "Model not found"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/api/reconstruction/refined_mesh/<model_id>')
def get_refined_mesh_data(model_id):
    current_app.logger.info(f"Getting refined mesh data for model: {model_id}")
    data = visualization_service.get_mesh_data(model_id, mesh_type='refined')
    if data is None:
        return jsonify({"error": "Model not found"}), 404
    return jsonify(data)

@api_bp.route('/api/reconstruction/textured_mesh/<model_id>')
def get_textured_mesh_data(model_id):
    current_app.logger.info(f"Getting textured mesh data for model: {model_id}")
    data = visualization_service.get_textured_mesh_data(model_id)
    if data is None:
        return jsonify({"error": "Model not found"}), 404
    return jsonify(data)

########################################################################
# Preprocess Visuals
########################################################################
@api_bp.route('/api/preprocess/<param>/<ply_id>')
def get_preprocess_process_ply(param, ply_id):
    current_app.logger.info(f"Getting {param} ply data for preprocess visuals: {ply_id}")
    data = preprocess_service.get_ply(ply_id, param)
    if data is None:
        return jsonify({"error": f"{param} ply not found"}), 404
    return jsonify([data])

