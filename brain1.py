import time
import requests
import numpy as np
import cv2
from ultralytics import YOLO

# ESP32 camera URL
BASE_URL = "http://192.168.1.31"

def get_image_snap():
    url_snap = BASE_URL + "/api/snap"
    try:
        response = requests.get(url_snap, timeout=2)
        if response.status_code == 200:
            img_array = np.frombuffer(response.content, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return img
        else:
            print("Failed to get image")
            return None
    except requests.exceptions.RequestException:
        print("Error connecting to camera")
        return None

def stop():
    url = BASE_URL + "/api/stop"
    try:
        res = requests.get(url, timeout=1)
        if res.status_code == 200:
            print("Robot stopped:", res.json().get('msg'))
        else:
            print("Stop command failed")
    except:
        print("Stop request error")

def forward():
    url = BASE_URL + "/api/forward"
    try:
        res = requests.get(url, timeout=1)
        if res.status_code == 200:
            print("Robot moving forward:", res.json().get('msg'))
        else:
            print("Forward command failed")
    except:
        print("Forward request error")

if __name__ == "__main__":
    model = YOLO("yolo12n.pt")  # Load YOLO model (you can use yolov8s.pt, etc.)
    moving = False  # Track robot state

    print("Press 'q' to quit the program.")
    
    while True:
        img = get_image_snap()
        if img is None:
            continue

        results = model(img)                                            # Detect objects with model
        names = results[0].names                                        # Get class names that can be detected by model
        detected = [names[int(cls)] for cls in results[0].boxes.cls]    # Organize detected class names as a list for ease of use later

        # Moving logic
        if 'person' in detected:                                        # Name of image detected to trigger a stop command
            if moving:      
                stop()      
                moving = False
        else:
            if not moving:
                forward()
                moving = True

        # Show the image (optional)
        bounded_img = results[0].plot()                                 # Generate the image with bounding boxes
        cv2.imshow("Robot Camera", bounded_img)                         # Display the image in am OpenCV window 
        if cv2.waitKey(1) & 0xFF == ord('q'):                           # Press 'q' to exit       
            break                                                       # Exit the main loop

    stop()                                                              # Stop robot before exiting
    cv2.destroyAllWindows()                                             # Close all OpenCV windows       
