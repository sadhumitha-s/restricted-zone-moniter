import cv2
import numpy as np

class ZoneMapper:
    def __init__(self, window_name="Map Restricted Zone"):
        self.window_name = window_name
        self.points = []
        self.done = False

    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))

    def map_zone(self, frame):
        """
        Displays the frame and allows the user to click points to draw a polygon.
        Press 'Enter' to finish drawing.
        """
        self.points = []
        self.done = False
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self._mouse_callback)

        display_frame = frame.copy()

        print("--- Zone Mapping ---")
        print("Click on the image to define the vertices of the restricted zone.")
        print("Press 'Enter' or 'Space' when you are done.")
        
        while not self.done:
            temp_frame = display_frame.copy()
            
            # Draw the points and lines
            if len(self.points) > 0:
                for i, point in enumerate(self.points):
                    cv2.circle(temp_frame, point, 5, (0, 0, 255), -1)
                    if i > 0:
                        cv2.line(temp_frame, self.points[i-1], point, (0, 255, 0), 2)
                
                # Draw a line from the last point to the mouse cursor (if we wanted to track mouse, 
                # but we'll just draw the closed polygon when done)
                if len(self.points) > 2:
                     cv2.line(temp_frame, self.points[-1], self.points[0], (0, 255, 0), 2)

            cv2.imshow(self.window_name, temp_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 13 or key == 32:  # Enter or Space
                if len(self.points) >= 3:
                    self.done = True
                else:
                    print("Please select at least 3 points to form a polygon.")
            elif key == ord('q') or key == 27: # Esc or q
                print("Mapping cancelled. Exiting.")
                cv2.destroyWindow(self.window_name)
                return []

        cv2.destroyWindow(self.window_name)
        print(f"Zone defined with {len(self.points)} points: {self.points}")
        return np.array(self.points, np.int32)
