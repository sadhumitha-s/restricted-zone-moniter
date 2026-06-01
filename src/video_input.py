import cv2
import threading
from queue import Queue
import time

class VideoInput:
    def __init__(self, source_path, resize_dim=(640, 480), queue_size=128):
        self.source_path = source_path
        self.resize_dim = resize_dim
        self.cap = cv2.VideoCapture(source_path)
        self.q = Queue(maxsize=queue_size)
        self.stopped = False
        self.thread = None

        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {source_path}")

    def start(self):
        self.thread = threading.Thread(target=self._update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def _update(self):
        while True:
            if self.stopped:
                return

            if not self.q.full():
                ret, frame = self.cap.read()
                if not ret:
                    self.stop()
                    return

                if self.resize_dim:
                    frame = cv2.resize(frame, self.resize_dim)
                
                self.q.put(frame)
            else:
                time.sleep(0.01)

    def read(self):
        if self.q.empty() and self.stopped:
            return None
        elif self.q.empty():
            # Wait briefly if not stopped but queue is empty
            time.sleep(0.01)
            if self.q.empty():
                return None
        return self.q.get()

    def running(self):
        return not self.stopped or not self.q.empty()

    def stop(self):
        self.stopped = True
        if self.thread and self.thread.is_alive() and threading.current_thread() != self.thread:
            self.thread.join(timeout=1.0)
        self.cap.release()
