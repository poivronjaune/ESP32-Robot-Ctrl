import cv2
import threading
import time
from ultralytics import YOLO

class RobotCam:
    def __init__(self, url="rtsp://thingino:thingino@192.168.1.29:554/ch1"):
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
            # TODO: Add logging system 
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
                print("Warning: Lost connection to the stream, attempting to reconnect...")
                break
                # TODO: Add logging system
                # cap.release()
                # time.sleep(1) # Wait before reconnecting
                # cap = cv2.VideoCapture(self.url)
                # if not cap.isOpened():
                #     # TODO: Add logging system
                #     print("Error: Reconnection failed, stopping.")
                #     self.running = False
                #     break
            
        cap.release()

    def get_latest_frame(self):
        # Return the most recently read frame
        return self.frame
    
    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

class RobotDetection:
    def __init__(self):
        self.model = YOLO("yolo12n.pt")  
        #self.obj_to_detect = [0, 16, 65] # 0:Person, 16:Dog, 65:Remote 
        self.obj_to_detect = [65]
        self.frame = None
        self.box_details = []

    def add_object_to_detect(self, id):
        pass
    
    def del_object_to_detect(self, id):
        pass
    
    def get_box_details(self):
        return self.box_details

    def detect_objects(self, frame):
        if frame is None:
            self.frame = None
            return None
        
        self.frame = frame
        results = self.model(frame, classes=self.obj_to_detect, verbose=False)
        
        boxes = results[0].boxes
        names = results[0].names # Get class names that can be detected by model

        if boxes is not None:
            for box in boxes:
                x1,y1, x2, y2 = map(int, box.xyxy[0]) # Get object coordintes
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])                            
                label = f"{names[cls_id]} {confidence:.2f}"
                box_detail = {"cls_id": cls_id, "x1": x1, "y1": y1, "x2": x2, "y2": y2, "label": label}
                self.box_details.append(box_detail)
        
        return len(self.box_details)
        
    def add_bounding_boxes(self) -> None:
        if len(self.box_details) < 1:
            return
        
        for box in self.box_details:
            cv2.rectangle(self.frame, (box.get("x1"), box.get("y1")), (box.get("x2"), box.get("y2")), (0,255,0), 2) # Draw box around the object
            (w, h), _ = cv2.getTextSize(box.get("label"), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(self.frame, (box.get("x1"), box.get("y1") - h - 5), (box.get("x1") + w, box.get("y1")), (0, 255, 0), -1) # Draw label background
            cv2.putText(self.frame, box.get("label"), (box.get("x1"), box.get("y1") - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA) # Draw label text
        
        return self.frame
        
    def flush(self):
        self.frame = None
        self.box_details = []
        
#    def augment_image(self, frame):
#        if frame is None:
#            return None
#        
#        results = self.model(frame, classes=self.obj_to_detect, verbose=False)
#        
#        boxes = results[0].boxes
#        names = results[0].names # Get class names that can be detected by model
#
#        if boxes is not None:
#            for box in boxes:
#                x1,y1, x2, y2 = map(int, box.xyxy[0]) # Get object coordintes
#                cls_id = int(box.cls[0])
#                confidence = float(box.conf[0])                            
#                label = f"{names[cls_id]} {confidence:.2f}"
#
#                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2) # Draw box around the object
#                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
#                cv2.rectangle(frame, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1) # Draw label background
#                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA) # Draw label text
#
#        return frame