import time, socket, network
import machine
from robot_server.config import SSID, PASSWORD
from robot_server.server import start_server

#from robot_server.vision import cam_esp32 as cam
#from robot_server.vision import cam_ip as cam
try:
    import camera
    camera.deinit() # Call this function to make sure camera does not have pre-run garbage
    esp32cam = True
except Exception as e:
     print(' 🛠 Skiping ESP32 Camera setup')
     esp32cam = False
# Change these settings for you specific Wifi
#SSID = 'Guest Slow'
#PASSWORD = 'FleursEtJardin'

# Setup Camera - 5 retries or fail
if esp32cam:
    for i in range(5):
        cam = camera.init()

        print(f"📷 Camera ready?: {cam}")
        if cam:
            print("📷 Camera initialized.")
            break
        else:
            time.sleep(2)    # Retry camera.init() in 2 seconds
    if not cam:
        print("📷 Camera setup failed")

    # Camera setup was succesful if cam is True
    if cam: 
        camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
        camera.contrast(2)       # increase contrast
        camera.speffect(2)       # jpeg grayscale

#Connect to network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
print('📡 Connecting to Wi-Fi...')
while not wifi.isconnected():
    time.sleep(1)
print(f'⚡ Connected, try: http://{wifi.ifconfig()[0]}:80/')

if cam:
    start_server()
else:
    start_server()
    print(' 🌐 Server started without an ESP32 Camera')

if esp32cam:
    camera.deinit()
    
machine.reset()



