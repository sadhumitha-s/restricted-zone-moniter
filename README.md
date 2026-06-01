# Restricted Zone Intrusion Detection System

## Overview
The Restricted Zone Intrusion Detection System is a computer vision application built for monitoring restricted areas, such as railway tracks. It uses state-of-the-art deep learning (YOLOv8) to automatically detect persons and animals, tracks their movement using ByteTrack, and determines their movement status (Moving vs. Stationary). 

This repository contains the Phase 1 implementation (Core Vision Pipeline), focusing on robust detection, consistent tracking, and real-time visualization from a local MP4 video file.

## Features
- **Object Detection**: Identifies 'Human' and general 'Animal' classes using YOLOv8n.
- **Object Tracking**: Assigns and maintains unique tracking IDs across frames.
- **Movement Classification**: Analyzes object trajectories over a short history to classify them as 'Moving' or 'Stationary'.
- **Live Visualization**: Displays a real-time annotated video feed with bounding boxes, dynamic color-coding (Blue for humans, Green for animals), and confidence scores.

## Project Structure
```text
restricted-zone-monitor/
├── main.py                 # Main orchestrator script
├── requirements.txt        # Python dependencies
├── src/
│   ├── video_input.py      # Background thread video ingestion & buffering
│   ├── detector.py         # YOLOv8n inference wrapper
│   └── tracker.py          # Movement state & tracking logic
├── tests/                  # Unit tests
├── videos/                 # Directory for local mp4 files
├── models/                 # Model weights directory
└── logs/                   # Directory for intrusion logs (Phase 3)
```

## Requirements & Installation
1. Ensure you have Python 3.9+ installed.
2. Clone the repository and navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using the main script. By default, it looks for a video file at `videos/sample.mp4`.

```bash
python main.py --source /path/to/your/video.mp4
```

Press `q` on your keyboard to stop the monitoring loop gracefully.
