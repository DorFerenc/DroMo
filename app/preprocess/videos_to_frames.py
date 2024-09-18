# app/preprocess/videos_to_frames.py
import cv2
import numpy as np
import os
from collections import defaultdict
from app.config import Config

class FrameExtractor:
    """
   A class to extract frames from a video based on object detection and frame quality.
   It uses the YOLO object detection model to detect objects and applies checks for frame quality
   (blur detection, lighting, and exposure).
   """
    def __init__(self):
        """
        Initialize the FrameExtractor with YOLO model and COCO labels.
        """
        # Load YOLO model
        self.net = cv2.dnn.readNet(Config.YOLO_WEIGHTS, Config.YOLO_CONFIG)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Load COCO dataset labels for YOLO
        with open(Config.COCO_NAMES, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect_object(self, frame):
        """
        Detect objects in the frame using the YOLO model.
       Parameters:
        - frame: np.array
            The frame in which to detect objects.
        Returns:
        - list: A list of tuples, where each tuple contains (class_id, confidence, (x, y, w, h))
                for each detected object.
       """
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)

        detections = self.net.forward(self.output_layers)
        objects = []

        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Threshold for detection confidence
                    # Get bounding box coordinates
                    center_x = int(obj[0] * width)
                    center_y = int(obj[1] * height)
                    w = int(obj[2] * width)
                    h = int(obj[3] * height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    objects.append((class_id, confidence, (x, y, w, h)))
        return objects

    def find_prominent_object(self, video_path, interval=20, sample_size=100):
        """
        Analyze a sample of frames to determine the most prominent object.

        Parameters:
        - video_path: str
            Path to the input video file.
        - interval: int, optional
            Interval (in frames) to check for object detection. Default is 20 frames.
        - sample_size: int, optional
            Number of frames to sample for detecting the prominent object. Default is 100 frames.

        Returns:
        - int: The class ID of the most prominent object.
        """
        cap = cv2.VideoCapture(video_path)
        frame_id = 0
        object_counter = defaultdict(int)

        sample_frames = 0
        while sample_frames < sample_size:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id % interval == 0:
                objects = self.detect_object(frame)
                for (class_id, confidence, (x, y, w, h)) in objects:
                    object_counter[class_id] += 1  # Track frequency
                sample_frames += 1
            frame_id += 1

        cap.release()
        # Determine the most prominent object by frequency or area
        # Choose based on which appears most often or has the largest total area
        if (len(object_counter) == 0):
            return None
        most_frequent_object = max(object_counter, key=object_counter.get)
        #largest_object = max(area_counter, key=area_counter.get)
        return most_frequent_object

    def is_frame_blurry(self, frame, threshold=100.0):
        """
        Check if the frame is blurry using the Laplacian variance method.

        Parameters:
        - frame: np.array
            The frame to check for sharpness.
        - threshold: float, optional
            Threshold for Laplacian variance below which a frame is considered blurry. Default is 100.0.

        Returns:
        - bool: True if the frame is blurry, otherwise False.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var < threshold

    def check_lighting(self, frame, min_brightness=50, max_brightness=200):
        """
       Check if the frame has good lighting, i.e., it's not too dark or too bright.

       Parameters:
       - frame: np.array
           The frame to check for lighting quality.
       - min_brightness: int, optional
           Minimum mean pixel intensity to consider the frame well-lit. Default is 50.
       - max_brightness: int, optional
           Maximum mean pixel intensity to consider the frame well-lit. Default is 200.

       Returns:
       - bool: True if the frame has good lighting, otherwise False.
       """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return min_brightness < mean_brightness < max_brightness

    def crop_to_object(self, frame, bbox):
        """
        Crop the frame to the detected object.

        Parameters:
        - frame: np.array
            The original frame.
        - bbox: tuple
            Bounding box coordinates (x, y, w, h) of the detected object.

        Returns:
        - cropped_frame: np.array
            The cropped frame containing only the detected object.
        """
        x, y, w, h = bbox
        return frame[y:y + h, x:x + w]  # Cropping the frame to the bounding box

    def apply_abominations(self, cropped_frame):
        """
        Apply custom transformations to the cropped frame for SfM.

        Parameters:
        - cropped_frame: np.array
            The frame that has been cropped to the detected object.

        Returns:
        - processed_frame: np.array
            The frame after applying various transformations.
        """
        # Resize to a standard size for SfM
        processed_frame = cv2.resize(cropped_frame, (640, 480))

        # Convert to grayscale (SIFT works better on grayscale images)
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur (optional, to smooth out noise)
        processed_frame = cv2.GaussianBlur(processed_frame, (5, 5), 0)

        # Enhance edges to help with feature extraction for SfM
        # processed_frame = cv2.Canny(processed_frame, 50, 150)

        return processed_frame

    def extract_frames_with_object(self, video_path, output_dir, prominent_object, interval=20):
        """
        Extract frames from the video where the most prominent object is detected.

        Parameters:
        - video_path: str
            Path to the input video file.
        - output_dir: str
            Directory where the extracted frames will be saved.
        - prominent_object: int
            The class ID of the most prominent object.
        - interval: int, optional
            Interval (in frames) to check for object detection. Default is 20 frames.

        Returns:
        - int: Total number of frames that were saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        frame_id = 0
        frames_count = 0
        last_detected_frame = -interval

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id - last_detected_frame >= interval:
                objects = self.detect_object(frame)
                for (class_id, confidence, (x, y, w, h)) in objects:
                    if class_id == prominent_object and not self.is_frame_blurry(frame) and self.check_lighting(frame):
                        # Crop the frame to the detected object
                        cropped_frame = self.crop_to_object(frame, (x, y, w, h))

                        # Apply additional transformations (abominations)
                        processed_frame = self.apply_abominations(cropped_frame)

                        output_path = os.path.join(output_dir, f"frame_{frame_id}.jpg")
                        cv2.imwrite(output_path, processed_frame)
                        last_detected_frame = frame_id
                        frames_count += 1
                        break  # Break after detecting the prominent object in the current frame

            frame_id += 1

        cap.release()
        return frames_count

    def extract_relevant_frames(self, video_path, output_dir, interval=20, sample_size=100):
        """
        Extract frames from a video based on the most prominent object detection and frame quality.

        Parameters:
        - video_path: str
            Path to the input video file.
        - output_dir: str
            Directory where the extracted frames will be saved.
        - interval: int, optional
            Interval (in frames) to check for object detection. Default is 20 frames.
        - sample_size: int, optional
            Number of frames to sample for detecting the prominent object. Default is 100 frames.

        Returns:
        - int: Total number of frames that were saved.
        """
        # First, find the most prominent object in the video
        prominent_object = self.find_prominent_object(video_path, interval, sample_size)
        if prominent_object == None:
            return None
        prominent_object_name = self.classes[prominent_object]
        print(f"The most prominent object is: {prominent_object_name}")
        # Then, extract frames where that prominent object appears
        return self.extract_frames_with_object(video_path, output_dir, prominent_object, interval)

