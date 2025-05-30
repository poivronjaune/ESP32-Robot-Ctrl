# config.py
# RTSP stream
RTSP_URL = "rtsp://thingino:thingino@192.168.1.36:554/ch1"
BASE_URL = "http://192.168.1.37/api"


# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
IMAGE_SIZE = 400
WINDOW_TITLE = "Robot Controller"

# Button settings
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 70
BUTTON_MARGIN = 10

# Button labels
BTN_LABEL_LEFT = "LEFT"
BTN_LABEL_UP = "UP"
BTN_LABEL_DOWN = "DOWN"
BTN_LABEL_RIGHT = "RIGHT"
BTN_LABEL_STOP = "STOP"

# Path to YOLOv12n model file
YOLO_MODEL_PATH = "yolo12n.pt"
DETECTION_INTERVAL = 5

# Colors
class colors:
    BLACK = (0, 0, 0)
    BLUE = (70, 70, 200)
    WHITE = (255, 255, 255)
