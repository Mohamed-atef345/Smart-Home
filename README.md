# Hand Gesture Control System with Arduino
This project allows users to control various functionalities (like volume control, finger counting, and light detection) using hand gestures detected through a webcam. The system communicates with an Arduino board via serial communication to execute different commands based on the detected gestures.

## Features:
*Finger Counting: Counts the number of raised fingers and sends the count to the Arduino.
*Volume Control: Adjusts the volume by measuring the distance between the thumb and index finger (pinching gesture).
*Light Detection: Reads light sensor data from the Arduino and displays it in the terminal.
*Temperature Detection: Reads temperature sensor data from the Arduino and displays it in the terminal.
*Red LED Control: Allows turning on and off a red LED on the Arduino.
## Components:
* Arduino Board: Communicates with the system via serial connection to control outputs (LED, buzzer, etc.).
* Webcam: Captures hand gestures for detection.
* OpenCV: Used for image processing and hand gesture recognition.
* MediaPipe: Used for detecting hand landmarks and tracking fingers in real-time.
## Technologies Used:
* Python: The main programming language used for the system.
* OpenCV: For real-time computer vision to capture and process hand gestures.
* MediaPipe: For hand gesture tracking and landmark detection.
* Serial Communication (pySerial): For communication between the Python script and Arduino.
* Arduino: Controls hardware based on commands received from the Python script.
## Requirements:
* Python 3.x
* OpenCV
* MediaPipe
* pySerial
* An Arduino board with a suitable circuit setup
