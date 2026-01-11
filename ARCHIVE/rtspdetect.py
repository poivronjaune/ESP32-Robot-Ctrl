import cv2
import time
import requests

# Configuration
rtsp_url = "rtsp://thingino:thingino@192.168.1.36:554/ch1"
stop_api_url = "http://192.168.1.31/api/stop"
HEADLESS = False  # Set to False if you want to see a preview of the video stream using cv2.imshow()

# Placeholder: Replace this with real object detection logic
def detect_target_object(frame):
    # Example: Always returns False
    # Replace with actual model inference
    return False

# Open RTSP stream
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("Error: Cannot open RTSP stream.")
    exit()

print("Stream opened. Press Ctrl+C to quit.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Stream lost. Reconnecting...")
            time.sleep(1)
            cap.release()
            cap = cv2.VideoCapture(rtsp_url)
            continue

        # Show preview if not in headless mode
        if not HEADLESS:
            cv2.imshow("Live Stream", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Detect objects in frame
        if detect_target_object(frame):
            print("Target object detected! Sending STOP command...")
            try:
                response = requests.get(stop_api_url, timeout=2)
                if response.ok:
                    print("STOP command sent successfully.")
                else:
                    print(f"Failed to send STOP command: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error sending STOP command: {e}")
            
            time.sleep(2)  # Prevent flooding the server

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cleaned up and closed.")
# Cleanup
