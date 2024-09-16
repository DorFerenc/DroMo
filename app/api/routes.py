"""API routes for the DROMO system."""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.services.video_service import VideoService
from bson import ObjectId
import os

api_bp = Blueprint('api', __name__)
video_service = VideoService()

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

@api_bp.route('/api/preprocess/<video_id>', methods=['POST'])
def process_video(video_id):
    """PreProcess the video"""
    result = video_service.process_video(video_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404

@api_bp.route('/api/preprocess/progress/<video_id>', methods=['GET'])
def progress_process_video(video_id):
    """PreProcess the video"""
    result = video_service.get_progress(video_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Video not found or invalid ID'}), 404
