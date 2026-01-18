import network
import socket
from robot_server import wheels

# Configure WiFi connection
SSID = 'Guest Slow'
PASSWORD = 'FleursEtJardin'

# UDP Configuration
UDP_IP = '0.0.0.0'  # Listen on all interfaces
UDP_PORT = 5005

def connect_wifi():
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        
        while not wlan.isconnected():
            pass
    
    print('WiFi connected!')
    print('IP address:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def start_udp_listener():
    """Start UDP listener"""
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    print(f'UDP listener started on port {UDP_PORT}')
    print('Waiting for messages...')
    
    try:
        while True:
            # Receive data (buffer size 1024 bytes)
            data, addr = sock.recvfrom(1024)
            cmd = data.decode()
            print(f'Received from {addr}: {cmd}')
            
            if cmd == "FORWARD":
                wheels.forward()
            if cmd == "STOP":
                wheels.stop()
            if cmd == "BACKWARD":
                wheels.backward()
            if cmd == "LEFT":
                wheels.left()
            if cmd == "RIGHT":
                wheels.right()
                
            
            # Optional: Send response back
            response = f'ACK-Marc: {cmd} succesful'
            sock.sendto(response.encode(), addr)
            
    except KeyboardInterrupt:
        print('\nStopping listener...')
    finally:
        sock.close()

# Main execution
if __name__ == '__main__':
    ip = connect_wifi()
    start_udp_listener()
