import time
import cv2
from robot.robot_config import URL_ROBOT_CTRL, URL_RTSP_FEED
from robot.robot_vision import RobotCam, RobotDetection
from robot.robot_motors import RobotControl

#URL_RTSP_FEED = 'rtsp://thingino:thingino@192.168.1.29:554/ch1'  # Robot IP Camera
#URL_ROBOT_CTRL = 'http://192.168.1.30/'

def main():
    # Initialize and start the robot camera buffer
    # Since using a seperate thread, wait until a frame is received to comfirm proper initialization
    cam_feed = RobotCam(URL_RTSP_FEED)
    cam_feed.start()
    print("🛠 - Robot camera streaming started...")
    while cam_feed.get_latest_frame() is None:
        time.sleep(0.1)
    print("🛠 - Robot camera received initial image...")

    robot_detection = RobotDetection()
    print("🛠 - Robot detection function activated...")

    robot_ctrl = RobotControl(URL_ROBOT_CTRL)
    print("🛠 - Robot movement controller activated...")
    time.sleep(2)
    robot_ctrl.execute('STOP')

    print('---------------------')
    print('use a,w,s,d and space to control robot movement')
    print('---------------------')

    while True:
        latest_frame = cam_feed.get_latest_frame()

        # latest_frame = robot_detection.augment_image(latest_frame)
        num_objects_found = robot_detection.detect_objects(latest_frame)
        if num_objects_found > 0:
            print(f"EMERGENCY STOP {robot_ctrl.execute('STOP')}")
            latest_frame = robot_detection.add_bounding_boxes()
            robot_detection.flush()

        cv2.imshow('Latest Thingino Frame', latest_frame)



        # Press 'q' to exit the loop
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('q') or key_pressed == 27: # ESC
            print(f"'q' pressed - stoping robot...")
            break
        elif key_pressed == ord(' '):
            print(f"{robot_ctrl.execute('STOP')}")
        elif key_pressed == ord('w'):
            print(f"{robot_ctrl.execute('FORWARD')}")
        elif key_pressed == ord('s'):
            print(f"{robot_ctrl.execute('BACKWARD')}")
        elif key_pressed == ord('a'):
            print(f"{robot_ctrl.execute('LEFT')}")        
        elif key_pressed == ord('d'):
            print(f"{robot_ctrl.execute('RIGHT')}")        


        ## Add a small delay if needed for CPU usage management
        time.sleep(0.01)

if __name__ == "__main__":
    main()

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