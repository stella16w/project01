# project01

## Soccer Commentary MVP

A simple system that generates audio commentary for short soccer video clips using computer vision and text-to-speech.

### Features

- **Object Detection**: Detects players and ball using YOLOv8
- **Event Detection**: Identifies shots, passes, and goal area activity
- **Commentary Generation**: Creates natural language commentary using templates
- **Text-to-Speech**: Converts commentary to audio using gTTS

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the system:
```bash
python main.py path/to/your/video.mp4
```

### How it Works

1. **Video Processing**: Extracts frames from the input video
2. **Object Detection**: Uses YOLOv8 to detect players and ball in each frame
3. **Event Analysis**: Analyzes movement patterns to identify game events
4. **Commentary Generation**: Selects appropriate commentary based on detected events
5. **Audio Output**: Converts text commentary to speech and plays it

### Supported Events

- **Shot**: Fast ball movement (>200 pixels/sec)
- **Pass**: Moderate ball movement (100-200 pixels/sec)  
- **Player Interaction**: Player within 50 pixels of ball
- **Goal Area Activity**: Ball detected in goal areas

### Requirements

- Python 3.7+
- OpenCV
- YOLOv8 (ultralytics)
- PyTorch
- gTTS (Google Text-to-Speech)
- pygame

### Example Usage

```bash
python main.py sample_soccer_clip.mp4
```

The system will:
1. Process the video clip
2. Detect players and ball movements
3. Identify key events
4. Generate appropriate commentary
5. Play the commentary as audio

### Limitations

- Works best with clear, well-lit soccer footage
- Optimized for short clips (10 seconds or less)
- Limited to basic event detection
- Commentary is template-based, not dynamic

### Future Enhancements

- More sophisticated event detection
- Dynamic commentary generation
- Multiple language support
- Real-time processing
- Custom voice options
