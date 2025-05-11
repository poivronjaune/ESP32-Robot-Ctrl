import time
import socket
import network
import machine
import camera
# from web_server import start_server
from robot_server.server import start_server

camera.deinit() # Call this function to make sure camera does not have pre-run garbage

# Change these settings for you specific Wifi
SSID = 'Guest Slow'
PASSWORD = 'FleursEtJardin'

# Setup Camera - 5 retries or fail
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
    print(' 🌐 Server not started - something went wrong (probably camera.init() failed)')

camera.deinit()
machine.reset()

