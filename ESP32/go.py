import time, socket, network
import machine
from robot_server.config import SSID, PASSWORD, HOSTNAME
from robot_server.server import start_server


#Connect to network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
time.sleep(1)

wifi.config(dhcp_hostname=HOSTNAME)


wifi.connect(SSID, PASSWORD)

print('📡 Connecting to Wi-Fi...')
while not wifi.isconnected():
    time.sleep(1)
ip_address = f'http://{wifi.ifconfig()[0]}:80/'
base_url = f'http://{network.hostname()}/'

print(f'⚡ Connected, try: {base_url}')
print(f'⚡ ip_address: {ip_address}')


start_server()
print(' 🌐 Server started without an ESP32 Camera')
   
machine.reset()



