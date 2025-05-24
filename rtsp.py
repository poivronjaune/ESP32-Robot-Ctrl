import cv2

# RTSP stream URL
rtsp_url = "rtsp://thingino:thingino@192.168.1.36:554/ch1"

# Open connection to the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the connection was successful
if not cap.isOpened():
    print("Error: Cannot open RTSP stream.")
    exit()

print("Connected to the RTSP stream. Press 'q' to quit.")

# Continuously read and display frames
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame. Reconnecting...")
        cap.release()
        cap = cv2.VideoCapture(rtsp_url)
        continue

    # Display the frame
    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
