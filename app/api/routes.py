"""API routes for the DROMO system."""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.db.mongodb import get_db
from app.services.video_service import VideoService
from app.models.point_cloud import PointCloud
from bson import ObjectId, errors as bson_errors
import os
# from app.services.reconstruction_service import ReconstructionService

api_bp = Blueprint('api', __name__)
video_service = VideoService()
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


# @api_bp.route('/api/reconstruct/<id>', methods=['POST'])
# def reconstruct(id):
#     """
#     Start the reconstruction process for a given point cloud.

#     Args:
#         id (str): Point Cloud ID

#     Returns:
#         JSON response with reconstruction status and model ID.
#     """
#     try:
#         # Assuming you have a method to get point cloud data by ID
#         point_cloud_data = video_service.get_point_cloud(id)

#         if not point_cloud_data:
#             return jsonify({"error": "Point cloud not found"}), 404

#         # Start the reconstruction process asynchronously
#         model_id = reconstruction_service.start_reconstruction(id, point_cloud_data)

#         return jsonify({
#             "message": "Reconstruction started",
#             "model_id": model_id
#         }), 200

#     except Exception as e:
#         current_app.logger.error(f"Reconstruction error: {str(e)}")
#         return jsonify({"error": "Internal server error"}), 500

