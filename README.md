# ESP32-Robot-Ctrl  
  
BROTHERS Hobby project for robotic Lawn Mower.  
The robot lawnmower **is not** autonomous, it requires an external program to implement the driving intelligence and object detection. It can be controlled using a web browser with very simple commands - mostly for testing.  

> **⚠️ Work in Progress:**  
> Not ready for production

[![Work in Progress](https://img.shields.io/badge/status-in_progress-yellow)](https://github.com/poivronjaune/ESP32-Robot-Ctrl)
![Last Commit](https://img.shields.io/github/last-commit/poivronjaune/ESP32-Robot-Ctrl)

---  

#     
# Introduction  
![image](/images/componentsV3.png)   

This project is divided in two main components.  
- The Robot itself with electronics, camera, motors, battery and blades  
- The External App that acts as the robot Brain to implement high level funtions to control the robot actions    

> Note: We chose to have an RTSP feed independant of the micro-controller for performance reasons. When both the motor controls and ESP32Cam were implemented on a single board too much lag was introduced in the system to work properly.  
> Instead of using an IP Camera, an ESP32CAM can be implemented but we recommend using two different micro-controllers.  


# Technologies
This project is designed for learning and fun. For this purpose we chose to implement most of the programming in [Python](https://www.python.org/) and/or [MicroPython](https://micropython.org/).  

## Hardware
- ESP32-S2 micro-controller based on the [espressif](https://www.espressif.com/en/products/socs/esp32-s2) hardware with the Camera package  
- An IP-Camera with an RTSP protocol OR an onboard ESP32-CAM that captures still images
- A battery  
- DC Motors  
- Motor controllers  
- Homemade Platform and wheels

## Robot controller 
- An ESP32 with a micropython firmware controls the motors and checks the battery level  
- The ESP32 connects to a WIFI network to permit communication from the external app (brain)  
- Through this WIFI connection a Webserver (using web sockets) exposes Robot APIs
- If an ESP32-CAM is used, an /api/snap route provides still image capturing as an HTTP connection, otherwise the external app must connect to the IP Camera's RTSP stream (optional)    

## Computer Brain
- A python program (or any other app that can use web requests)  
- Connects to the robot controller's web server using it's IP Address  
- Sends commands to move, stop, turn, start/stop blade, get battery level and snap images for object detection  
- Controls the mowing path and detects yard limits    
- Analyses the image capture to only move over grass and avoid objects  
- Returns to charging station when battery is too low  
- Offers a manual driving interface  

# Setup  
- See the section Flashing Micro-python on ESP32 for details
- Assemble a robot base and connect motors, battery and all electronics
- Configure network SSID and PASSWORD in the robot_server/config.py file and upload all micropython files to the ESP32 (see upload scripts to micro-python)
- Launch the robot_server on the robot controller using go.py
- Configure the external app (brain.py) to connect to the IP adress of the web server and RTSP feed of the IP camera
- Run the python app on your computer

# Micropython Webserver  
- The python code for the robot controller has a main function called go.py to lauch the robot_server (manually)
- A file called main.py, will be launched automatically but offers a small delay to CTRL-BREAK to the REPL when connected directly to the serial port
- The rest of the code is organized in modules under the "robot_server" package.  
- The server.py module starts a web server through web sockets connections and implements simple routes decorator and render_template (similar to flask)  
- The routes.py module uses the @routes(path) decorator to implement API commands and other web pages  
- The wheels.py module contains all control functions for the motors
- The templates folder contains all HTML pages to render 
- The static folder stores CSS files and some default images  

# Flashing Micropython firmware  
Some implementations could use a basic ESP32 Camera. A micropython firmware that includes the camera module is provided to get you started.  

Tutorialsfor Flashing firmware:  
Flash micropython with ESPTOOL from [Random Nerd](https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/)

> Micropython firmware for ESP32-CAM is inpired by shariltumin's github project->  [esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022)   

Latest [Generic ESP32 Firmware](https://micropython.org/download/ESP32_GENERIC/)


```
py -m pip install esptool
cd ESP32\firmware
py -m esptool write_flash 0x1000 ESP32_GENERIC-20251209-v1.27.0.bin
```

# Uploading Scripts to micro-python
Use [Thonny](https://thonny.org/) to connect to EPS32 and upload python files to micro-controller  

# Installing the robot package
More details Coming soon  
```
py -3.13 -m venv .venv
.venv\script\actiavte
py pip -m pip install -e .
```
  
Change values in the robot\robot_config.py to reflect your local area network connections for IP Camera and ESP32 Processor.  
Change preferred YOLO Object detection [model](https://docs.ultralytics.com/models/)  

# YOLO Model Objects
Default model is 12n (yolo12n.pt) COCO Dataset objects detectable without training.  
Class names:  
  0: person  
  1: bicycle  
  2: car  
  3: motorcycle  
  4: airplane  
  5: bus  
  6: train  
  7: truck  
  8: boat  
  9: traffic light  
  10: fire hydrant  
  11: stop sign  
  12: parking meter  
  13: bench  
  14: bird  
  15: cat  
  16: dog  
  17: horse  
  18: sheep  
  19: cow  
  20: elephant  
  21: bear  
  22: zebra  
  23: giraffe  
  24: backpack  
  25: umbrella  
  26: handbag  
  27: tie  
  28: suitcase  
  29: frisbee  
  30: skis  
  31: snowboard  
  32: sports ball  
  33: kite  
  34: baseball bat  
  35: baseball glove  
  36: skateboard  
  37: surfboard  
  38: tennis racket  
  39: bottle  
  40: wine glass  
  41: cup  
  42: fork  
  43: knife  
  44: spoon  
  45: bowl  
  46: banana  
  47: apple  
  48: sandwich  
  49: orange  
  50: broccoli  
  51: carrot  
  52: hot dog  
  53: pizza  
  54: donut  
  55: cake  
  56: chair  
  57: couch  
  58: potted plant  
  59: bed  
  60: dining table  
  61: toilet  
  62: tv  
  63: laptop  
  64: mouse  
  65: remote  
  66: keyboard  
  67: cell phone  
  68: microwave  
  69: oven  
  70: toaster  
  71: sink  
  72: refrigerator  
  73: book  
  74: clock  
  75: vase  
  76: scissors  
  77: teddy bear  
  78: hair drier  
  79: toothbrush  