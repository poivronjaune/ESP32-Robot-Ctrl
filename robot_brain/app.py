import time
import requests
BASE_URL = "http://192.168.1.31"

def snap():
    url_snap = BASE_URL + "/snap"

    res = requests.get(url_snap)
    if res.status_code == 200:
        with open("snap.jpg", "wb") as f:
            f.write(res.content)
        print("Image saved as snap.jpg")

def stop():
    url_stop = BASE_URL + "/api/stop"
    res = requests.get(url_stop)
    
    if res.status_code == 200:
        print("Robot stopped")
        print(res.json().get('msg'))
    else:
        print("Robot response error")

def forward():
    url_stop = BASE_URL + "/api/forward"
    res = requests.get(url_stop)
    
    if res.status_code == 200:
        print("Robot forward")
        print(res.json().get('msg'))
    else:
        print("Robot response error")

def backward():
    url_stop = BASE_URL + "/api/backward"
    res = requests.get(url_stop)
    
    if res.status_code == 200:
        print("Robot backward")
        print(res.json().get('msg'))
    else:
        print("Robot response error")


if __name__ == "__main__":
    stop()
    input('Press Enter to move forward')
    forward()
    input('Press Enter to move backward')
    backward()
    input('Press Enter to stop')
    stop()
    