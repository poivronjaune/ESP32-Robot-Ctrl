import time, socket, network
import machine
from robot_server.config import SSID, PASSWORD
from robot_server.server import start_server


#Connect to network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print('📡 Connecting to Wi-Fi...')
while not wifi.isconnected():
    time.sleep(1)
base_url = f'http://{wifi.ifconfig()[0]}:80/'
print(f'⚡ Connected, try: {base_url}')

start_server()
print(' 🌐 Server started without an ESP32 Camera')
   
machine.reset()



