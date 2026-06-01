import cv2
import argparse
import sys
import os

from src.video_input import VideoInput
from src.detector import Detector
from src.tracker import MovementTracker

def main():
    parser = argparse.ArgumentParser(description="Restricted Zone Monitor - Phase 1")
    parser.add_argument("--source", type=str, default="videos/sample.mp4", help="Path to input MP4 video file")
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"Error: Video file {args.source} not found.")
        print("Please place a sample video at that location or specify the path with --source.")
        sys.exit(1)

    print(f"Initializing video input from {args.source}...")
    video_stream = VideoInput(args.source).start()

    print("Loading YOLOv8 detector...")
    detector = Detector()

    movement_tracker = MovementTracker()

    print("Starting monitoring. Press 'q' to quit.")
    
    while video_stream.running():
        frame = video_stream.read()
        if frame is None:
            continue
            
        results = detector.track(frame)
        
        active_track_ids = []
        
        if results.boxes is not None and results.boxes.id is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            track_ids = results.boxes.id.int().cpu().tolist()
            class_ids = results.boxes.cls.int().cpu().tolist()
            confidences = results.boxes.conf.cpu().numpy()
            
            for box, track_id, class_id, conf in zip(boxes, track_ids, class_ids, confidences):
                # Ensure the class is allowed
                if class_id not in detector.ALLOWED_CLASSES:
                    continue
                
                active_track_ids.append(track_id)
                
                label = detector.get_class_label(class_id)
                status = movement_tracker.update_and_get_status(track_id, box)
                
                # Dynamic coloring: Human = Blue, Animal = Green
                color = (255, 0, 0) if label == "Human" else (0, 255, 0)
                
                x1, y1, x2, y2 = map(int, box)
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Overlay text: Label, Status, Conf, ID
                text = f"{label} #{track_id} ({status}) {conf:.2f}"
                cv2.putText(frame, text, (x1, max(y1 - 10, 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Cleanup old tracks to free memory
        movement_tracker.cleanup_old_tracks(active_track_ids)

        # Display the frame
        cv2.imshow("Restricted Zone Monitor", frame)
        
        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    video_stream.stop()
    cv2.destroyAllWindows()
    print("Monitoring stopped.")

if __name__ == "__main__":
    main()
