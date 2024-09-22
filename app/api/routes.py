"""API routes for the DROMO system."""

from flask import Blueprint, request, jsonify, current_app, send_file, abort, Response
from werkzeug.utils import secure_filename
from app.db.mongodb import get_db
from app.services.video_service import VideoService
from app.services.reconstruction_service import ReconstructionService
from app.models.point_cloud import PointCloud
from app.models.threed_model import ThreeDModel
from app.services.preprocess_service import PreprocessService
from bson import ObjectId, errors as bson_errors
import os
import traceback


api_bp = Blueprint('api', __name__)
video_service = VideoService()
preprocess_service = PreprocessService()
# reconstruction_service = ReconstructionService()


# @api_bp.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Welcome to the DROMO API"}), 200

# @api_bp.route('/api/upload', methods=['POST'])
@api_bp.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_visual_data():
    """
    Handle the upload of visual data.

    Expects:
        - A 'file' in the request files
        - A 'title' in the form data (optional)

    Returns:
        JSON response with upload status and video ID.
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

        video_id = video_service.create_video(title, file_path)

        return jsonify({
            "message": "Upload success",
            "video_id": video_id
        }), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

def allowed_file(filename):
    """
    Check if the file extension is allowed.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@api_bp.route('/api/videos/<video_id>', methods=['GET'])
def get_video(video_id):
    """Retrieve information about a specific video."""
    video = video_service.get_video(video_id)
    if video:
        return jsonify({
            'id': str(video['_id']),
            'title': video['title'],
            'file_path': video['file_path'],
            'timestamp': video['timestamp'] #.isoformat()
        }), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404


@api_bp.route('/api/videos', methods=['GET'])
def list_videos():
    """List all videos."""
    videos = video_service.get_all_videos()
    return jsonify([{
        'id': str(video['_id']),
        'title': video['title'],
        'timestamp': video['timestamp'] # .isoformat()
    } for video in videos]), 200


@api_bp.route('/api/videos/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Delete a specific video."""
    result = video_service.delete_video(video_id)
    if result:
        return jsonify({'message': 'Video deleted successfully'}), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404

########################################################################
# Pre Process api
########################################################################

@api_bp.route('/api/preprocess/<video_id>', methods=['POST'])
def process_video(video_id):
    """
        PreProcess the video
        Args:
            video_id (str): The id of the video to preprocess.
        Returns:
            dict: The processed video data if found, None otherwise.
        """
    result = preprocess_service.process_ply(video_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404

@api_bp.route('/api/preprocess/progress/<video_id>', methods=['GET'])
def progress_process_video(video_id):
    """PreProcess the video"""
    result = preprocess_service.get_progress(video_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404

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
def get_point_cloud(point_cloud_id):
    """Retrieve a specific point cloud."""
    try:
        object_id = ObjectId(point_cloud_id)
    except bson_errors.InvalidId:
        return jsonify({'error': 'Invalid point cloud ID'}), 400

    db = get_db()
    pc_data = db.point_clouds.find_one({'_id': object_id})

    if pc_data:
        return jsonify({
            'id': str(pc_data['_id']),
            'name': pc_data['name'],
            'num_points': len(pc_data['points']),
            'has_colors': 'colors' in pc_data,
            'timestamp': pc_data['timestamp'].isoformat()
        }), 200
    else:
        return jsonify({'error': 'Point cloud not found'}), 404

@api_bp.route('/api/point_clouds', methods=['GET'])
def list_point_clouds():
    """List all point clouds."""
    db = get_db()
    point_clouds = db.point_clouds.find()
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
        model_id = ReconstructionService.start_reconstruction(point_cloud_id)

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
    model = ThreeDModel.get_by_id(model_id)
    if model and model.obj_file:
        file_path = os.path.join(model.folder_path, model.obj_file)
        if os.path.exists(file_path):
            return send_file(file_path)
    abort(404)




# @api_bp.route('/api/models/<model_id>/<filename>', methods=['GET'])
# def get_model_file(model_id, filename):
#     """Serve model files (OBJ, MTL, or texture)."""
#     model = ThreeDModel.get_by_id(model_id)
#     if not model:
#         abort(404, description="Model not found")

#     file_path = os.path.join(model.folder_path, filename)
#     if not os.path.exists(file_path):
#         abort(404, description=f"File {filename} not found for model {model_id}")

#     return send_file(file_path)