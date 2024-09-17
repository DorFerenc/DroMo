"""Application configuration."""

import os
from datetime import timedelta

class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/dromo')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

    # YOLO model configuration
    YOLO_WEIGHTS = '/app/yolov3/yolov3.weights'
    YOLO_CONFIG = '/app/yolov3/yolov3.cfg'
    COCO_NAMES = '/app/yolov3/coco.names'
    # YOLO_WEIGHTS = os.path.join(os.path.dirname(__file__), '/app/yolov3/yolov3.weights')
    # YOLO_CONFIG = os.path.join(os.path.dirname(__file__), '/app/yolov3/yolov3.cfg')
    # COCO_NAMES = os.path.join(os.path.dirname(__file__), '/app/yolov3/coco.names')
