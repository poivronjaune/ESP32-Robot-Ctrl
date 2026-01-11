import cv2
import threading
import time
from ultralytics import YOLO

class RTSPVideoBuffer:
    def __init__(self, url):
        self.url = url
        self.frame = None
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        # Open the RTSP stream
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print(f"Error: Could not open video stream {self.url}")
            self.running = False
            return

        while self.running:
            # Read the next frame
            ret, frame = cap.read()
            if ret:
                # Update the shared frame variable with the latest frame
                self.frame = frame
            else:
                # Break the loop if reading fails
                print("Warning: Lost connection to the stream, attempting to reconnect...")
                cap.release()
                time.sleep(1) # Wait before reconnecting
                cap = cv2.VideoCapture(self.url)
                if not cap.isOpened():
                    print("Error: Reconnection failed, stopping.")
                    self.running = False
                    break
            
        cap.release()

    def get_latest_frame(self):
        # Return the most recently read frame
        return self.frame
    
    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

# --- Example Usage ---
RTSP_URL = 'rtsp://thingino:thingino@192.168.1.29:554/ch1' # Replace with your actual Thingino RTSP URL

# 0. Initialize and start the buffer
video_buffer = RTSPVideoBuffer(RTSP_URL)
video_buffer.start()

print("Streaming started. Waiting for the first frame...")
# Wait until a frame is received
while video_buffer.get_latest_frame() is None:
    time.sleep(0.1)

model = YOLO("yolo12n.pt") 

try:
    while True:
        # 1. Get the latest frame when you need it
        latest_frame = video_buffer.get_latest_frame()
        
        # 2. Process the frame (e.g., display it, analyze it, save it)
        if latest_frame is not None:
            # Example: Display the frame (optional)
        
            results = model(latest_frame, classes=[0, 16, 65]) # 0:Person, 16:Dog, 65:remote
            
            boxes = results[0].boxes
            names = results[0].names # Get class names that can be detected by model
            
            if boxes is not None:
                for box in boxes:
                    x1,y1, x2, y2 = map(int, box.xyxy[0]) # Get object coordintes
                    cls_id = int(box.cls[0])
                    confidence = float(box.conf[0])                            
                    label = f"{names[cls_id]} {confidence:.2f}"
            
                    cv2.rectangle(latest_frame, (x1,y1), (x2,y2), (0,255,0), 2) # Draw box around the object
                    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(latest_frame, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1) # Draw label background
                    cv2.putText(latest_frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA) # Draw label text

            # detected = [names[int(cls)] for cls in results[0].boxes.cls]    # Organize detected class names as a list for ease of use later
            # print("Detectable objects:", detected)          
        
            cv2.imshow('Latest Thingino Frame', latest_frame)
            
            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Add a small delay if needed for CPU usage management
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    # 4. Stop the buffer and close windows
    video_buffer.stop()
    cv2.destroyAllWindows()
    print("Streaming stopped and resources released.")


# YOLO Object names
# 0: person
# 1: bicycle
# 2: car
# 3: motorcycle
# 4: airplane
# 5: bus
# 6: train
# 7: truck
# 8: boat
# 9: traffic light
# 10: fire hydrant
# 11: stop sign
# 12: parking meter
# 13: bench
# 14: bird
# 15: cat
# 16: dog
# 17: horse
# 18: sheep
# 19: cow
# 20: elephant
# 21: bear
# 22: zebra
# 23: giraffe
# 24: backpack
# 25: umbrella
# 26: handbag
# 27: tie
# 28: suitcase
# 29: frisbee
# 30: skis
# 31: snowboard
# 32: sports ball
# 33: kite
# 34: baseball bat
# 35: baseball glove
# 36: skateboard
# 37: surfboard
# 38: tennis racket
# 39: bottle
# 40: wine glass
# 41: cup
# 42: fork
# 43: knife
# 44: spoon
# 45: bowl
# 46: banana
# 47: apple
# 48: sandwich
# 49: orange
# 50: broccoli
# 51: carrot
# 52: hot dog
# 53: pizza
# 54: donut
# 55: cake
# 56: chair
# 57: couch
# 58: potted plant
# 59: bed
# 60: dining table
# 61: toilet
# 62: tv
# 63: laptop
# 64: mouse
# 65: remote
# 66: keyboard
# 67: cell phone
# 68: microwave
# 69: oven
# 70: toaster
# 71: sink
# 72: refrigerator
# 73: book
# 74: clock
# 75: vase
# 76: scissors
# 77: teddy bear
# 78: hair drier
# 79: toothbrush