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
![image](/images/componentsV2.png)   

This project is divided in two main components.  
- The Robot itself with electronics, camera, motors, battery and blades  
- The External App that acts as the robot Brain to implement high level funtions to control the robot actions    

See our [Read The Docs Pages](https://about.readthedocs.com/) [Coming soon] for in depth documentation.  

# Technologies
This project is designed for learning and fun. For this purpose we chose to implement most of the programming in [Python](https://www.python.org/) and/or [MicroPython](https://micropython.org/).  

## Hardware
- ESP32-S2 micro-controller based on the [espressif](https://www.espressif.com/en/products/socs/esp32-s2) hardware with the Camera package  
- An IP-Camera with an RTSP protocol OR an onboard ESP32-CAM that captures still images
- A battery  
- DC Motors  
- Motor controllers  
- DIY Platform and wheels

## Robot controller 
- An ESP32 with a micropython firmware controls the motors and checks the battery level  
- The ESP32 connects to a WIFI network to permit communication from the external app  
- Through this WIFI connection a Webserver (using web sockets) exposes Robot APIs
- If an ESP32-CAM is used, an /pi/snap route provides still image capturing as an HTTP connection, otherwise the external app must connect to the IP Camera's RTSP stream  

## Computer Brain
- A python program (or any other app that can use web requests)  
- Connects to the robot controller's web server using it's IP Address  
- Sends commands to move, stop, turn, start/stop blade, get battery level and snap images for object detection  
- Controls the mowing path and detects yard limits    
- Analyses the image capture to only move over grass and avoid objects  
- Returns to charging station when battery is too low  
- Offers a manual driving interface  

# Setup  
- Assemble a robot base and connect motors, battery and all electronics
- Configure network SSID and PASSWORD in the robot_server/config.py file and upload all micropython files to the ESP32 (thonny was used for this task)  
- Launch the robot_server on the robot controller using go.py
- Configure the external app (brain.py) to connect to the IP adress of the web server and RTSP feed of the IP camera
- Run the python app on your computer

See the detailed documentation (***coming when project will be viable***) 

# Micropython Webserver  
- The python code for the robot controller has a main function called go.py to lauch the robot_server
- The rest of the code is organized in modules under the "robot_server" package.  
- The server.py module starts a web server through web sockets connections and implements simple routes decorator and render_template (similar to flask)  
- The routes.py module uses the @routes(path) decorator to implement API commands and other web pages  
- The wheels.py module contains all control functions for the motors
- The templates folder contains all HTML pages to render 
- The static folder stores CSS files and some default images  

# Micropython firmware  
Some implementations could use a basic ESP32 Camera. A micropython firmware that includes the camera module is provided to get you started.  

> Micropython firmware for ESP32-CAM is inpired by shariltumin's github project->  [esp32-cam-micropython-2022](https://github.com/shariltumin/esp32-cam-micropython-2022)   
