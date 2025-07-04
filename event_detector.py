import numpy as np
import math

class EventDetector:
    def __init__(self):
        self.events = []
        
    def calculate_distance(self, pos1, pos2):
        """Calculate distance between two positions"""
        if pos1 is None or pos2 is None:
            return float('inf')
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def detect_ball_movement(self, detections):
        """Detect ball movement patterns"""
        ball_positions = []
        
        for detection in detections:
            if detection['ball']:
                ball_positions.append({
                    'frame': detection['frame'],
                    'position': detection['ball']['center'],
                    'timestamp': detection['timestamp']
                })
        
        if len(ball_positions) < 3:
            return []
        
        events = []
        
        # Detect fast ball movement (potential shot/pass)
        for i in range(1, len(ball_positions)):
            prev_pos = ball_positions[i-1]['position']
            curr_pos = ball_positions[i]['position']
            
            distance = self.calculate_distance(prev_pos, curr_pos)
            time_diff = ball_positions[i]['timestamp'] - ball_positions[i-1]['timestamp']
            
            if time_diff > 0:
                speed = distance / time_diff
                
                # Fast movement detected
                if speed > 100:  # Threshold for fast movement
                    event_type = "shot" if speed > 200 else "pass"
                    events.append({
                        'type': event_type,
                        'timestamp': ball_positions[i]['timestamp'],
                        'frame': ball_positions[i]['frame'],
                        'description': f"Ball moving at {speed:.1f} pixels/sec"
                    })
        
        return events
    
    def detect_player_interactions(self, detections):
        """Detect player-ball interactions"""
        events = []
        
        for detection in detections:
            if not detection['ball'] or not detection['players']:
                continue
            
            ball_pos = detection['ball']['center']
            
            # Check if any player is close to the ball
            for player in detection['players']:
                player_pos = player['center']
                distance = self.calculate_distance(ball_pos, player_pos)
                
                if distance < 50:  # Close interaction threshold
                    events.append({
                        'type': 'player_interaction',
                        'timestamp': detection['timestamp'],
                        'frame': detection['frame'],
                        'description': f"Player near ball (distance: {distance:.1f})"
                    })
                    break
        
        return events
    
    def detect_goal_area_activity(self, detections, frame_width, frame_height):
        """Detect activity near goal areas"""
        events = []
        
        # Define goal areas (assuming horizontal field view)
        left_goal = (0, frame_height * 0.3, frame_width * 0.1, frame_height * 0.7)
        right_goal = (frame_width * 0.9, frame_height * 0.3, frame_width, frame_height * 0.7)
        
        for detection in detections:
            if not detection['ball']:
                continue
            
            ball_pos = detection['ball']['center']
            
            # Check if ball is in goal area
            if (left_goal[0] < ball_pos[0] < left_goal[2] and 
                left_goal[1] < ball_pos[1] < left_goal[3]):
                events.append({
                    'type': 'goal_area_activity',
                    'timestamp': detection['timestamp'],
                    'frame': detection['frame'],
                    'description': "Ball in left goal area"
                })
            elif (right_goal[0] < ball_pos[0] < right_goal[2] and 
                  right_goal[1] < ball_pos[1] < right_goal[3]):
                events.append({
                    'type': 'goal_area_activity',
                    'timestamp': detection['timestamp'],
                    'frame': detection['frame'],
                    'description': "Ball in right goal area"
                })
        
        return events
    
    def analyze_events(self, detections, frame_width=1920, frame_height=1080):
        """Analyze all events in the video"""
        all_events = []
        
        # Detect different types of events
        ball_events = self.detect_ball_movement(detections)
        interaction_events = self.detect_player_interactions(detections)
        goal_events = self.detect_goal_area_activity(detections, frame_width, frame_height)
        
        all_events.extend(ball_events)
        all_events.extend(interaction_events)
        all_events.extend(goal_events)
        
        # Sort events by timestamp
        all_events.sort(key=lambda x: x['timestamp'])
        
        return all_events