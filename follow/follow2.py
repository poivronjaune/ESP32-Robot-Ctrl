import cv2
import requests
from ultralytics import YOLO

RTSP_URL = "rtsp://thingino:thingino@192.168.1.36:554/ch1"
BASE_URL = "http://192.168.1.37/api"

def connect_robot_controller():
    try:
        response = requests.get(BASE_URL, timeout=5)
        response.raise_for_status()
        print(f"Successfully connected to robot controller at: {BASE_URL}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to robot controller at {BASE_URL}: {e}")
        return False

def connect_rtsp_feed():
    cap = cv2.VideoCapture(RTSP_URL)
    if cap.isOpened():
        print(f"Successfully connected to RTSP feed at: {RTSP_URL}")
        return cap
    else:
        print(f"Error: Could not open RTSP stream at {RTSP_URL}")
        return None

def load_yolo_model(model_name='yolo12n.pt'):
    try:
        model = YOLO(model_name)
        print(f"YOLO model '{model_name}' loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading YOLO model '{model_name}': {e}")
        return None

def draw_boxes(frame, results):
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f"{result.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

if __name__ == "__main__":
    robot_connected = connect_robot_controller()
    rtsp_capture = connect_rtsp_feed()
    yolo_model = load_yolo_model()

    if robot_connected and rtsp_capture is not None and yolo_model is not None:
        print("Initial setup complete. Starting video stream...")
        while True:
            ret, frame = rtsp_capture.read()
            if not ret:
                print("Failed to grab frame from RTSP stream.")
                break

            results = yolo_model.predict(frame, conf=0.25, iou=0.45, classes=None, agnostic_nms=True)

            # Draw results
            annotated_frame = draw_boxes(frame, results)

            # Show the frame
            cv2.imshow("YOLO12n Detection", annotated_frame)

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        rtsp_capture.release()
        cv2.destroyAllWindows()
    else:
        print("Failed to connect to one or more components.")

