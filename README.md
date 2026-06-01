# Restricted Zone Intrusion Detection System

## Overview
The Restricted Zone Intrusion Detection System is a computer vision application built for monitoring restricted areas, such as railway tracks. It uses state-of-the-art deep learning (YOLOv8) to automatically detect persons and animals, tracks their movement using ByteTrack, and determines their movement status (Moving vs. Stationary). 

This repository implements the complete end-to-end system, which includes the Core Vision Pipeline, Spatial Logic & Intrusion Detection, and Evidence Collection & Analytics capabilities.

## Features
- **Object Detection**: Identifies 'Human' and general 'Animal' classes using YOLOv8n.
- **Object Tracking**: Assigns and maintains unique tracking IDs across frames.
- **Movement Classification**: Analyzes object trajectories over a short history to classify them as 'Moving' or 'Stationary'.
- **Interactive Zone Mapping**: Provides an interactive UI to click and draw a polygon representing the restricted zone on the first frame of the video.
- **Intrusion Detection**: Uses spatial logic to determine if an object's bottom-center point has entered the restricted zone.
- **Live Visualization**: Displays a real-time annotated video feed with bounding boxes, dynamic color-coding (Red for intrusions, Blue for humans, Green for animals), and a semi-transparent overlay of the restricted zone.
- **Evidence Collection**: Logs detailed intrusion events (time, duration, type, etc.) to a persistent CSV file.
- **Summary Analytics**: Automatically calculates and displays summary statistics on application exit.

## Project Structure
```text
restricted-zone-monitor/
├── main.py                 # Main orchestrator script
├── requirements.txt        # Python dependencies
├── src/
│   ├── video_input.py      # Background thread video ingestion & buffering
│   ├── detector.py         # YOLOv8n inference wrapper
│   ├── tracker.py          # Movement state & tracking logic
│   ├── zone_mapper.py      # UI logic to interactively map the restricted zone
│   ├── zone_checker.py     # Spatial logic to detect zone intrusions
│   ├── logger.py           # Intrusion event logging to CSV
│   └── statistics.py       # Generation of summary analytics from logs
├── tests/                  # Unit tests (including test_zone_checker.py)
├── videos/                 # Directory for local mp4 files
├── models/                 # Model weights directory
└── logs/                   # Directory for intrusion logs
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

### Steps:
1. When you run the script, a static window will pop up showing the first frame of the video.
2. Click at least 3 points on the image to draw a polygon representing your restricted zone.
3. Press `Enter` or `Space` to confirm the zone. (Press `q` or `Esc` to cancel and proceed without a zone).
4. The live monitoring will start. Press `q` on your keyboard to stop the monitoring loop gracefully.
5. Upon exit, a summary of all intrusions will be printed to the console, and detailed event records are saved in `logs/intrusion_log.csv`.

## License
All rights reserved.
