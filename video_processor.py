import cv2
import numpy as np
from ultralytics import YOLO

class VideoProcessor:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.ball_positions = []
        self.player_positions = []
        
    def extract_frames(self, video_path):
        """Extract frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames
    
    def detect_objects(self, frame):
        """Detect players and ball in frame"""
        results = self.model(frame, verbose=False)
        
        players = []
        ball = None
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    if conf > 0.5:  # Confidence threshold
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        
                        # Person class (assuming players)
                        if cls == 0:
                            players.append({
                                'bbox': (x1, y1, x2, y2),
                                'center': (center_x, center_y),
                                'confidence': conf
                            })
                        # Sports ball class
                        elif cls == 32:
                            ball = {
                                'bbox': (x1, y1, x2, y2),
                                'center': (center_x, center_y),
                                'confidence': conf
                            }
        
        return players, ball
    
    def track_movement(self, frames):
        """Track ball and player movements across frames"""
        all_detections = []
        
        for i, frame in enumerate(frames):
            players, ball = self.detect_objects(frame)
            
            detection = {
                'frame': i,
                'players': players,
                'ball': ball,
                'timestamp': i / 30.0  # Assume 30fps
            }
            all_detections.append(detection)
        
        return all_detections