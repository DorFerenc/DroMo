# app/preprocess/visual_datas_to_frames.py
import cv2
import numpy as np
import os
from app.config import Config

class FrameExtractor:
    def __init__(self):
        # Load YOLO model
        self.net = cv2.dnn.readNet(Config.YOLO_WEIGHTS, Config.YOLO_CONFIG)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # Load COCO dataset labels for YOLO
        with open(Config.COCO_NAMES, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect_object(self, frame):
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)

        detections = self.net.forward(self.output_layers)

        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Threshold for detection confidence
                    return True  # Object detected
        return False  # No object detected

    def extract_relevant_frames(self, visual_data_path, output_dir, interval=20):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.visual_dataCapture(visual_data_path)
        frame_id = 0
        frames_count = 0
        last_detected_frame = -interval

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id - last_detected_frame >= interval:
                object_detected = self.detect_object(frame)
                if object_detected:
                    output_path = os.path.join(output_dir, f"frame_{frame_id}.jpg")
                    cv2.imwrite(output_path, frame)
                    last_detected_frame = frame_id
                    frames_count += 1

            frame_id += 1

        cap.release()
        return frames_count  # Return total number of frames processed
