from .server import route, render_template
from . import wheels
# import time
import json
# import ubinascii
# import gc

#### Common header for most HTML responses ####
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

def header_json(payload_size):
    header  = f"HTTP/1.1 200 OK\r\n"
    header += f"Content-Type: application/json\r\n"
    header += f"Content-Length: {payload_size}\r\n"
    header += f"Connection: close\r\n"
    header += f"\r\n"
    
    return header



@route("/")
def index():
    context = {
        "title": "ESP32 Home",
        "heading": "BROTHERS Robot Controller!",
        "message": "Served by a MicroPython ESP32 web server."
    }

    http_header = header_200()
    return http_header + render_template("home.html", context)


#@route("/drive")
#def drive():
#    context = {
#        "title": "ESP32 Drive",
#        "heading": "BROTHERS Robot Controller",
#        "message": "_"
#    }          
#    http_header = header_200()
#    return http_header + render_template("drive.html", context)
    

def default_api_response(msg):
    json_response = {
        "status": "success",
        "code": 200,
        "msg": msg
    }
    
    payload = json.dumps(json_response)
    http_header = header_json(len(payload))

    return http_header + payload

@route("/api")
def api_stop():
    # Return a web page (using render_template), not a JSON response
    context = {
        "title": "ESP32 Drive",
        "heading": "BROTHERS Robot Controller",
        "message": '<a href="/api/stop">stop</a> | <a href="/api/forward">forward</a> | <a href="/api/backward">backward</a> | <a href="/api/left">left</a> | <a href="/api/right">right</a>'
    }
    
    http_header = header_200()
    return http_header + render_template("api.html", context)


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

@route("/api/left")
def api_left():
    wheels.left()
    json_response = default_api_response("LEFT TURN")
    return json_response

@route("/api/right")
def api_right():
    wheels.right()
    json_response = default_api_response("RIGHT TURN")
    return json_response


