import cv2
import numpy as np
import time

class ZoneChecker:
    def __init__(self, polygon_points, logger=None):
        """
        Initializes the ZoneChecker with a predefined polygon.
        
        Args:
            polygon_points (np.ndarray): Array of polygon points.
            logger (EventLogger, optional): Logger for tracking intrusion events.
        """
        self.polygon = polygon_points
        self.logger = logger
        # Dictionary to keep track of active intrusions: {track_id: {data dict}}
        self.active_intrusions = {}
        
        # Debounce settings
        # To avoid flickering at the boundary, an object could be required to be inside
        # for a certain number of frames or time, but for the MVP, we just track entry/exit.
        
    def _get_bottom_center(self, bounding_box):
        """
        Calculates the bottom-center point of a bounding box.
        
        Args:
            bounding_box (list or tuple): [x1, y1, x2, y2]
            
        Returns:
            tuple: (x_center, y_bottom)
        """
        x1, y1, x2, y2 = bounding_box
        x_center = (x1 + x2) / 2
        y_bottom = y2
        return (int(x_center), int(y_bottom))

    def check_intrusion(self, track_id, bounding_box, label="Unknown", status="Unknown", conf=0.0):
        """
        Checks if the object is inside the restricted zone and updates intrusion state.
        
        Args:
            track_id (int): Unique ID of the tracked object.
            bounding_box (list or tuple): [x1, y1, x2, y2]
            label (str): Class label of the object.
            status (str): Movement status.
            conf (float): Detection confidence.
            
        Returns:
            bool: True if the object is currently inside the zone, False otherwise.
        """
        if self.polygon is None or len(self.polygon) == 0:
            return False
            
        point = self._get_bottom_center(bounding_box)
        
        # cv2.pointPolygonTest returns > 0 if inside, 0 if on contour, < 0 if outside
        is_inside = cv2.pointPolygonTest(self.polygon, point, False) >= 0
        
        if is_inside:
            if track_id not in self.active_intrusions:
                # New entry
                self.active_intrusions[track_id] = {
                    'entry_time': time.time(),
                    'label': label,
                    'status': status,
                    'conf': conf
                }
        else:
            if track_id in self.active_intrusions:
                # Exit
                track_data = self.active_intrusions.pop(track_id)
                exit_time = time.time()
                duration = exit_time - track_data['entry_time']
                
                if self.logger:
                    event_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exit_time))
                    entry_time_str = time.strftime('%H:%M:%S', time.localtime(track_data['entry_time']))
                    exit_time_str = time.strftime('%H:%M:%S', time.localtime(exit_time))
                    
                    self.logger.log_event(
                        event_time=event_time_str,
                        object_id=track_id,
                        object_type=track_data['label'],
                        movement_status=track_data['status'],
                        confidence=track_data['conf'],
                        entry_time=entry_time_str,
                        exit_time=exit_time_str,
                        duration=duration
                    )
                
        return is_inside

    def cleanup_old_tracks(self, active_track_ids):
        """
        Removes tracks that are no longer active to prevent memory leaks.
        """
        lost_tracks = []
        for track_id in list(self.active_intrusions.keys()):
            if track_id not in active_track_ids:
                lost_tracks.append(track_id)
                
        for track_id in lost_tracks:
            track_data = self.active_intrusions.pop(track_id)
            exit_time = time.time()
            duration = exit_time - track_data['entry_time']
            
            if self.logger:
                event_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exit_time))
                entry_time_str = time.strftime('%H:%M:%S', time.localtime(track_data['entry_time']))
                exit_time_str = time.strftime('%H:%M:%S', time.localtime(exit_time))
                
                self.logger.log_event(
                    event_time=event_time_str,
                    object_id=track_id,
                    object_type=track_data['label'],
                    movement_status=track_data['status'],
                    confidence=track_data['conf'],
                    entry_time=entry_time_str,
                    exit_time=exit_time_str,
                    duration=duration
                )

    def flush_active_intrusions(self):
        """
        Force closes all active intrusions, useful when shutting down the system.
        """
        self.cleanup_old_tracks([])

    def has_active_intrusions(self):
        """
        Returns True if there is at least one active intrusion.
        """
        return len(self.active_intrusions) > 0
        
    def draw_zone(self, frame):
        """
        Draws the restricted zone on the frame.
        Green if safe, Red if an intrusion is active.
        """
        if self.polygon is None or len(self.polygon) == 0:
            return frame
            
        overlay = frame.copy()
        
        # Determine color based on intrusion status
        if self.has_active_intrusions():
            color = (0, 0, 255)  # Red
        else:
            color = (0, 255, 0)  # Green
            
        cv2.fillPoly(overlay, [self.polygon], color)
        
        # Blend the overlay with the original frame (semi-transparent)
        alpha = 0.3
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Draw the solid outline
        cv2.polylines(frame, [self.polygon], isClosed=True, color=color, thickness=2)
        
        return frame
