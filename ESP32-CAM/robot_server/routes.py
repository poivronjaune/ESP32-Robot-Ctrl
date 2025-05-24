from .server import route, render_template
from . import wheels
import time
import json
import ubinascii
import gc

try:
    import camera
    esp32cam = True
except:
    esp32cam = False

#### Common header for most HTML pages ####
def header_200():
    header  = "HTTP/1.1 200 OK\r\n"
    header += "Content-Type: text/html\r\n"
    header += "Connection: close\r\n"
    header += "\r\n"
    return header

def header_jpeg(payload_size):
    header  = f"HTTP/1.1 200 OK\r\n"
    header += f"Content-Type: image/jpeg\r\n"
    header += f"Content-Length: {payload_size}\r\n"
    header += f"Connection: close\r\n"
    header += f"\r\n"
    # If calling function sends back raw byte image data, must be converted to bytes using .encode()
    return header

@route("/")
def index():
    context = {
        "title": "ESP32 Home",
        "heading": "BROTHERS Robot Controller!",
        "message": "Served by a MicroPython ESP32 web server."
    }
    #return render_template("index.html", context)
    http_header = header_200()
    return http_header + render_template("home.html", context)

@route("/about")
def about():
    context = {
        "title": "ESP32 About",
        "heading": "BROTHERS Robot Controller",
        "message": "Served by a MicroPython ESP32 web server."
    }    
    http_header = header_200()
    return http_header + render_template("page.html", context)

@route("/stop")
def stop():
    wheels.stop()
    context = {
        "title": "ESP32 Drive",
        "heading": "BROTHERS Robot Controller",
    }      
    http_header = header_200()
    return http_header + render_template("drive.html", context)

@route("/forward")
def forward():
    context = {
        "title": "ESP32 Drive",
        "heading": "BROTHERS Robot Controller",
    }          
    wheels.forward()
    http_header = header_200()
    return http_header + render_template("drive.html", context)

@route("/backward")
def backward():
    wheels.backward()
    context = {
        "title": "ESP32 Drive",
        "heading": "BROTHERS Robot Controller",
    }          
    http_header = header_200()
    return http_header + render_template("drive.html", context)

@route("/drive")
def drive():
    context = {
        "title": "ESP32 Drive",
        "heading": "BROTHERS Robot Controller",
    }          
    http_header = header_200()
    return http_header + render_template("drive.html", context)
    
@route("/image")
def image():
    context = {
        "title": "ESP32 Image",
        "heading": "BROTHERS Robot Controller (Image display)",
    }
    http_header = header_200()
    return http_header + render_template("image.html", context)


#### API Calls ####
# Helper functions to simplify coding in routes (with a JSON response and json response header)
def header_json(payload_size):
    header  = f"HTTP/1.1 200 OK\r\n"
    header += f"Content-Type: application/json\r\n"
    header += f"Content-Length: {payload_size}\r\n"
    header += f"Connection: close\r\n"
    header += f"\r\n"
    
    return header

def default_api_response(msg):
    json_response = {
        "status": "success",
        "code": 200,
        "msg": msg
    }

    payload = json.dumps(json_response)
    http_header = header_json(len(payload))

    return http_header + payload

@route("/api/stop")
def api_stop():
    wheels.stop()
    json_response = default_api_response("STOP")
    return json_response

@route("/api/forward")
def api_stop():
    wheels.forward()
    json_response = default_api_response("FORWARD")
    return json_response

@route("/api/backward")
def api_stop():
    wheels.backward()
    json_response = default_api_response("BACKWARD")
    return json_response

@route("/api/snap")
def snap():
    if esp32cam:
        img_data = camera.capture()
        raw_data = camera.capture() # Raw byte code for image
        time.sleep_ms(100)
    else:
        base_dir = "/".join(__file__.split("/")[:-1])
        nocamera_img_file = "/".join([base_dir, "static", "nocamera.jpg"])

        with open(nocamera_img_file, "r") as f:
            raw_data = f.read()
    
    http_header = header_jpeg(len(raw_data))
    
    return http_header.encode() + raw_data

