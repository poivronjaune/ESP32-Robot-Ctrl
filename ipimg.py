import sys
import requests
import cv2
import numpy as np

url = "http://thingino:thingino@192.168.0.237/image.jpg"  # Replace with actual URL

response = requests.post(url)

print("Status code:", response.status_code)


#img = response.text
img = response.content

#display img
img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
cv2.imshow("Image", img)    
cv2.waitKey(0)
cv2.destroyAllWindows()
