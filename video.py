import cv2
from ultralytics import YOLO
import numpy as np
model = YOLO("yolov8n.pt")
sources = {
    "0": 0,
    "rtsp": "rtsp://your_url",
    "file": "video.mp4"
}
cap = cv2.VideoCapture(0)
detection_enabled = True

def set_source(source_name):
    global cap
    if source_name in sources:
        cap.release()
        cap = cv2.VideoCapture(sources[source_name])
        return True
    return False

def toggle_detection():
    global detection_enabled
    detection_enabled = not detection_enabled
    return detection_enabled

def generate_video():
    global cap, detection_enabled
    while True:
        success, frame = cap.read()
        if not success:
            continue

        if detection_enabled:
            results = model.predict(frame, conf=0.5)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    if label not in ["cat", "person"]:
                        continue
                    conf = box.conf[0]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

