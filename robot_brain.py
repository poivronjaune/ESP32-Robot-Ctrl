import time
import cv2
from robot_vision import RobotCam, RobotDetection
from robot_motors import RobotControl

URL_RTSP_FEED = 'rtsp://thingino:thingino@192.168.1.29:554/ch1'  # Robot IP Camera
URL_ROBOT_CTRL = 'http://192.168.1.30/'

# Initialize and start the robot camera buffer
# Since using a seperate thread, wait until a frame is received to comfirm proper initialization
cam_feed = RobotCam(URL_RTSP_FEED)
cam_feed.start()
print("🛠 - Robot camera streaming started...")
while cam_feed.get_latest_frame() is None:
    time.sleep(0.1)
print("🛠 - Robot camera received initial image...")

robot_ctrl = RobotControl(URL_ROBOT_CTRL)
print(robot_ctrl.forward())
time.sleep(2)
robot_ctrl.stop()

robot_detection = RobotDetection()
while True:
    latest_frame = cam_feed.get_latest_frame()

    latest_frame = robot_detection.augment_image(latest_frame)
    
    cv2.imshow('Latest Thingino Frame', latest_frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    ## Add a small delay if needed for CPU usage management
    time.sleep(0.01)


############## UI ICONS ###############
# 📷 — Camera status and messages
# 📡 — Internet connectivity
# ⚡ — Running
# 🌐 — System message
# 🛑 — Debug
# 🛠 — Configuration messages
# ⛔ — Stop, Error, Logging
# 🤖 — Robot status / autonomous mode
# 🔋 — Battery level / charging state
# 🔌 — Docked / charging station connected
# 🚧 — Obstacle detected / restricted area
# 🧭 — Navigation / GPS / positioning
# 🌱 — Mowing / grass cutting in progress
# ⏸️ — Paused / waiting
# ▶️ — Start / resume operation
# ❗ — Warning / attention needed
# 🔄 — Returning to dock / recalculating path