import requests

BASE_URL = "http://192.168.1.37/api"

def forward():
    requests.get(f"{BASE_URL}/forward")

def backward():
    requests.get(f"{BASE_URL}/backward")

def turn_left():
    requests.get(f"{BASE_URL}/left")

def turn_right():
    requests.get(f"{BASE_URL}/right")

def stop():
    requests.get(f"{BASE_URL}/stop")

def send_command(direction: str):
    direction = direction.lower()
    if direction == "up":
        forward()
    elif direction == "down":
        backward()
    elif direction == "left":
        turn_left()
    elif direction == "right":
        turn_right()
    elif direction == "stop":
        stop()
