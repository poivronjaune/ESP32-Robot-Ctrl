import cv2
import requests
from ultralytics import YOLO

RTSP_URL = "rtsp://thingino:thingino@192.168.1.36:554/ch1"
BASE_URL = "http://192.168.1.37/api"

def connect_robot_controller():
    """
    Attempts to connect to the robot controller.
    Prints a success message if the base URL is reachable.
    Returns True if connection is successful, False otherwise.
    """
    try:
        response = requests.get(BASE_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Successfully connected to robot controller at: {BASE_URL}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to robot controller at {BASE_URL}: {e}")
        return False

def connect_rtsp_feed():
    """
    Attempts to connect to the RTSP feed.
    Prints a success message if the feed can be opened.
    Returns the cv2.VideoCapture object if successful, None otherwise.
    """
    cap = cv2.VideoCapture(RTSP_URL)
    if cap.isOpened():
        print(f"Successfully connected to RTSP feed at: {RTSP_URL}")
        return cap
    else:
        print(f"Error: Could not open RTSP stream at {RTSP_URL}")
        return None

def load_yolo_model(model_name='yolo12n.pt'):
    """
    Loads the specified YOLO model.
    Returns the loaded YOLO model object.
    """
    try:
        model = YOLO(model_name)
        print(f"YOLO model '{model_name}' loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading YOLO model '{model_name}': {e}")
        return None

if __name__ == "__main__":
    robot_connected = connect_robot_controller()
    rtsp_capture = connect_rtsp_feed()
    yolo_model = load_yolo_model()

    if robot_connected and rtsp_capture is not None and yolo_model is not None:
        print("Initial setup complete.")
        if rtsp_capture.isOpened():
            rtsp_capture.release() # Release the capture object as we are not in the loop yet
    else:
        print("Failed to connect to one or more components.")