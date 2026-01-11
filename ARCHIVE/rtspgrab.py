import cv2
import time

# RTSP stream URL
rtsp_url = "rtsp://thingino:thingino@192.168.1.36:554/ch1"

# Open the stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Cannot open RTSP stream.")
    exit()

print("Press SPACE to capture a frame, 'q' to quit.")

while True:
    # Read and discard frames until keypress
    ret, frame = cap.read()

    if not ret:
        print("Stream lost. Reconnecting...")
        time.sleep(1)
        cap.release()
        cap = cv2.VideoCapture(rtsp_url)
        continue

    # Show current frame (preview)
    cv2.imshow("Live Stream (Press SPACE to capture)", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):  # Space bar pressed
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"frame_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Captured and saved: {filename}")

    elif key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
