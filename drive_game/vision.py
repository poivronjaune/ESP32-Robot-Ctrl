from ultralytics import YOLO
import cv2
import config

# Load YOLO model once
model = YOLO(config.YOLO_MODEL_PATH)

# Only detect 'person' class
TARGET_CLASS = 'cup'
#TARGET_CLASS_ID = model.names.index(TARGET_CLASS)
TARGET_CLASS_ID = next(k for k, v in model.names.items() if v == TARGET_CLASS)

def detect_people(frame):
    """
    Run YOLO object detection on a BGR frame, return list of boxes for 'person'.
    """
    results = model.predict(frame, imgsz=320, verbose=False)[0]
    boxes = []

    for box in results.boxes:
        if int(box.cls) == TARGET_CLASS_ID:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            boxes.append((x1, y1, x2, y2))

    return boxes

def draw_boxes(frame, boxes):
    """
    Draws green bounding boxes on a BGR frame.
    """
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, TARGET_CLASS, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame
