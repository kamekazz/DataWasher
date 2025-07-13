import os
import cv2
import base64
import threading
import time
from datetime import datetime
from queue import Queue, Empty
from pyzbar import pyzbar

from flask import current_app
from models import db, PalletLog


class BarcodeTracker:
    """Assigns a stable ID to each seen barcode."""

    def __init__(self):
        self._next = 1
        self._seen = {}  # barcode -> id

    def update(self, detections):
        results = []
        for code, (x, y, w, h) in detections:
            if code not in self._seen:
                self._seen[code] = self._next
                self._next += 1
            tid = self._seen[code]
            results.append((tid, code, (x, y, w, h)))
        return results


class DetectionService(threading.Thread):
    """Background thread grabbing frames and detecting barcodes."""

    def __init__(self, frame_queue):
        super().__init__(daemon=True)
        self.frame_queue = frame_queue
        self.running = threading.Event()
        pass_env = os.getenv("CAMERA_PASS")
        ip = os.getenv("CAMERA_IP")
        self.stream_url = (
            f"rtsp://admin:{pass_env}@{ip}:554/h264Preview_01_main"
            if pass_env and ip
            else None
        )
        self.cap = None
        self.tracker = BarcodeTracker()

    def reconnect(self):
        if self.cap:
            self.cap.release()
        if not self.stream_url:
            return False
        self.cap = cv2.VideoCapture(self.stream_url)
        return self.cap.isOpened()

    def run(self):
        self.running.set()
        while self.running.is_set():
            if not self.cap or not self.cap.isOpened():
                if not self.reconnect():
                    time.sleep(5)
                    continue
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            detections = []
            for barcode in pyzbar.decode(frame):
                x, y, w, h = barcode.rect
                code = barcode.data.decode("utf-8")
                detections.append((code, (x, y, w, h)))
            tracked = self.tracker.update(detections)
            # draw boxes
            for tid, code, (x, y, w, h) in tracked:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{tid}:{code}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
                # log to DB
                with current_app.app_context():
                    log = PalletLog(
                        pallet_id=code,
                        timestamp=datetime.utcnow(),
                        x=x + w // 2,
                        y=y + h // 2,
                    )
                    db.session.add(log)
                    db.session.commit()
            _, buf = cv2.imencode(".jpg", frame)
            b64 = base64.b64encode(buf).decode("utf-8")
            try:
                self.frame_queue.put_nowait(b64)
            except Exception:
                pass
        if self.cap:
            self.cap.release()

    def stop(self):
        self.running.clear()

