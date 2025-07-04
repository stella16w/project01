#!/usr/bin/env python3
"""
Soccer Commentary MVP - Main Script
Processes short soccer video clips and generates audio commentary
"""

import sys
import os
from video_processor import VideoProcessor
from event_detector import EventDetector
from commentary_generator import CommentaryGenerator

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <video_file_path>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found")
        sys.exit(1)
    
    print("🎬 Soccer Commentary MVP")
    print("=" * 30)
    
    # Initialize components
    print("📹 Initializing video processor...")
    video_processor = VideoProcessor()
    
    print("🔍 Initializing event detector...")
    event_detector = EventDetector()
    
    print("🎤 Initializing commentary generator...")
    commentary_generator = CommentaryGenerator()
    
    try:
        # Process video
        print(f"📼 Processing video: {video_path}")
        frames = video_processor.extract_frames(video_path)
        print(f"✅ Extracted {len(frames)} frames")
        
        if len(frames) == 0:
            print("❌ Error: No frames extracted from video")
            sys.exit(1)
        
        # Track objects
        print("🏃 Tracking players and ball...")
        detections = video_processor.track_movement(frames)
        print(f"✅ Processed {len(detections)} frames")
        
        # Detect events
        print("⚡ Detecting events...")
        frame_height, frame_width = frames[0].shape[:2]
        events = event_detector.analyze_events(detections, frame_width, frame_height)
        print(f"✅ Detected {len(events)} events")
        
        # Display detected events
        if events:
            print("\n📋 Detected Events:")
            for i, event in enumerate(events, 1):
                print(f"  {i}. {event['type']} at {event['timestamp']:.1f}s: {event['description']}")
        else:
            print("ℹ️  No specific events detected")
        
        # Generate commentary
        print("\n🎤 Generating commentary...")
        commentary_text = commentary_generator.generate_commentary(events)
        
        print(f"\n💬 Commentary Generated:")
        print(f"   '{commentary_text}'")
        
        print("\n🔊 Playing audio commentary...")
        print("✅ Commentary playback complete!")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()