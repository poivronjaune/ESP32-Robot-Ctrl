import socket
import time
import cv2
from robot.robot_config import URL_ROBOT_CTRL, URL_RTSP_FEED
from robot.robot_vision import RobotCam, RobotDetection
from robot.robot_motors import RobotControl

UDP_IP = "192.168.0.249"  # Replace with your device's IP
UDP_PORT = 5005
MESSAGE = "STOP"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

# Receive response
data, addr = sock.recvfrom(1024)
print(f"Received: {data.decode()}")

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
#robot_ctrl.execute('STOP')
sock.sendto("STOP".encode(), (UDP_IP, UDP_PORT))

print('---------------------')
print('use a,w,s,d and space to control robot movement')
print('---------------------')

running = True
while running:
    latest_frame = cam_feed.get_latest_frame()

    # latest_frame = robot_detection.augment_image(latest_frame)
    num_objects_found = robot_detection.detect_objects(latest_frame)
    if num_objects_found > 0:
        print(f"EMERGENCY STOP....")
        sock.sendto("STOP".encode(), (UDP_IP, UDP_PORT))
        
        latest_frame = robot_detection.add_bounding_boxes()
        robot_detection.flush()

    cv2.imshow('Latest Thingino Frame', latest_frame)

    # Press 'q' to exit the loop
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q') or key_pressed == 27:
        print(f"'q' pressed - stoping robot...")
        break
    elif key_pressed == ord(' '):
        sock.sendto("STOP".encode(), (UDP_IP, UDP_PORT))
    elif key_pressed == ord('w'):
        sock.sendto("FORWARD".encode(), (UDP_IP, UDP_PORT))
    elif key_pressed == ord('s'):
        sock.sendto("BACKWARD".encode(), (UDP_IP, UDP_PORT))
    elif key_pressed == ord('a'):
        sock.sendto("LEFT".encode(), (UDP_IP, UDP_PORT))
    elif key_pressed == ord('d'):
        sock.sendto("RIGHT".encode(), (UDP_IP, UDP_PORT))
    
    

sock.close()