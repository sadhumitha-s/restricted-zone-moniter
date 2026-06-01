import math
from collections import defaultdict

class MovementTracker:
    def __init__(self, history_length=15, movement_threshold=15.0):
        self.history_length = history_length
        self.movement_threshold = movement_threshold
        # dictionary mapping track_id to a list of (x, y) centroids
        self.track_history = defaultdict(list)

    def update_and_get_status(self, track_id, bbox):
        """
        bbox: [x1, y1, x2, y2]
        Returns: "Moving" or "Stationary"
        """
        # Calculate centroid
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0

        history = self.track_history[track_id]
        history.append((cx, cy))

        # Keep only the latest `history_length` frames
        if len(history) > self.history_length:
            history.pop(0)

        # Need at least a few frames to determine movement
        if len(history) < 5:
            return "Stationary"

        # Calculate distance between oldest and newest centroid in history
        old_cx, old_cy = history[0]
        new_cx, new_cy = history[-1]

        distance = math.sqrt((new_cx - old_cx)**2 + (new_cy - old_cy)**2)

        if distance > self.movement_threshold:
            return "Moving"
        return "Stationary"
        
    def cleanup_old_tracks(self, active_track_ids):
        """
        Remove track histories for objects that are no longer active
        """
        stale_ids = set(self.track_history.keys()) - set(active_track_ids)
        for track_id in stale_ids:
            del self.track_history[track_id]
