from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO(model_path)
        
        # COCO class mapping
        self.HUMAN_CLASS_ID = 0
        self.ANIMAL_CLASS_IDS = {14, 15, 16, 17, 18, 19, 20, 21, 22, 23}
        self.ALLOWED_CLASSES = [self.HUMAN_CLASS_ID] + list(self.ANIMAL_CLASS_IDS)

    def track(self, frame):
        """
        Runs object detection and tracking on the given frame.
        Uses YOLOv8's built-in ByteTrack implementation.
        """
        results = self.model.track(
            frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            classes=self.ALLOWED_CLASSES, 
            verbose=False
        )
        return results[0]

    def get_class_label(self, class_id):
        if class_id == self.HUMAN_CLASS_ID:
            return "Human"
        elif class_id in self.ANIMAL_CLASS_IDS:
            return "Animal"
        return "Unknown"
