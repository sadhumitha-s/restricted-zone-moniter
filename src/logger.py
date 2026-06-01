import csv
import os
from datetime import datetime

class EventLogger:
    def __init__(self, log_file="logs/intrusion_log.csv"):
        self.log_file = log_file
        self.headers = [
            "Event Time", "Object ID", "Object Type", 
            "Movement Status", "Confidence", "Entry Time", 
            "Exit Time", "Duration"
        ]
        self._ensure_log_file()

    def _ensure_log_file(self):
        """Ensure the log directory and file exist with headers."""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        file_exists = os.path.exists(self.log_file)
        
        if not file_exists:
            try:
                with open(self.log_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.headers)
            except Exception as e:
                print(f"Error creating log file: {e}")

    def log_event(self, event_time, object_id, object_type, movement_status, confidence, entry_time, exit_time, duration):
        """
        Log an intrusion event to the CSV file.
        """
        row = [
            event_time, object_id, object_type, movement_status, 
            f"{confidence:.2f}", entry_time, exit_time, f"{duration:.2f}"
        ]
        try:
            with open(self.log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
        except Exception as e:
            print(f"Error writing to log file: {e}")
