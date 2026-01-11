import time
import requests
import numpy as np
import cv2
from ultralytics import YOLO

BASE_URL = "http://192.168.1.30"
#IPCAM_URL = "http://thingino:thingino@192.168.1.36/image.jpg" 
IPCAM_URL = "http://thingino:thingino@192.168.1.29/image.jpg" # This link grabs a large 1920x1080 pixels image



def get_image_snap():
    #url_snap = BASE_URL + "/api/snap"
    url_snap = IPCAM_URL
    try:
        response = requests.get(url_snap)
        if response.status_code == 200:
            img_array = np.frombuffer(response.content, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            #img = cv2.resize(img, (400, 200))
            return img
        else:
            print("Failed to get image")
            return None
    except requests.exceptions.RequestException:
        print("Error connecting to camera")
        return None

def get_latest_frame():
    pass

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


def main():
    model = YOLO("yolo12n.pt")  # Load YOLO model (you can use yolov8s.pt, etc.)
    moving = False  # Track robot state

    print("Press 'q' to quit the program.")
    
    while True:
        #img = get_image_snap()
        img = get_latest_frame()
        if img is None:
            continue

        results = model(img, classes=[0])                               # Detect person objects with model
        names = results[0].names                                        # Get class names that can be detected by model
        detected = [names[int(cls)] for cls in results[0].boxes.cls]    # Organize detected class names as a list for ease of use later
        print("Detectable objects:", detected)                          # Print detected objects

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

if __name__ == "__main__":
    main()