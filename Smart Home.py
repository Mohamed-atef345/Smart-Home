import serial
#import finger_count as finger
#import buzzer_volume as buzzer
import time
import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize serial communication with Arduino on COM4 at 9600 baud rate
arduino = serial.Serial('COM4', 9600)
time.sleep(3)  # Wait for Arduino to initialize

# Function to control volume based on hand gesture distance (finger pinch)
def volume(length):
    """
    This function sends a volume control signal to Arduino based on the distance
    between the thumb and the index finger.
    
    Parameters:
        length (float): The distance between thumb and index finger.
    """
    if length < 30:
        arduino.write('1'.encode())  # Send command '1' for low volume
    elif length < 60:
        arduino.write('2'.encode())  # Send command '2' for medium-low volume
    elif length < 100:
        arduino.write('3'.encode())  # Send command '3' for medium volume
    elif length < 150:
        arduino.write('4'.encode())  # Send command '4' for medium-high volume
    elif length < 200:
        arduino.write('5'.encode())  # Send command '5' for high volume

# Main loop for controlling the Arduino based on user input
while True:
    command = input('Enter command: ')  # Wait for user command

    if command == 'l':
        # Start the finger counting program
        arduino.write('l'.encode())  # Notify Arduino to start counting fingers
        
        # Camera setup for hand tracking
        width_cam, height_cam = 900, 600
        capture = cv2.VideoCapture(0)
        capture.set(3, width_cam)
        capture.set(4, height_cam)

        # Initialize MediaPipe hands detection
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpdraw = mp.solutions.drawing_utils
        tipIds = [4, 8, 12, 16, 20]  # Landmark IDs for finger tips

        while True:
            success, img = capture.read()  # Capture frame from webcam
            img = cv2.flip(img, 1)  # Flip image horizontally for natural hand gestures

            # Process the image with MediaPipe
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            lmList = []  # List to store landmark coordinates

            if results.multi_hand_landmarks:
                # Iterate through detected hands
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                        mpdraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                        
                        # Highlight landmark points (optional)
                        if True:
                            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                    
                    # Finger counting logic
                    if len(lmList) == 21:
                        fingers = []
                        # Check if thumb is up
                        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                        # Check if other fingers are up
                        for tip in range(1, 5):
                            if lmList[tipIds[tip]][2] < lmList[tipIds[tip] - 2][2]:
                                fingers.append(1)
                            else:
                                fingers.append(0)

                        totalFingers = fingers.count(1)  # Count the number of raised fingers
                        arduino.write(str(totalFingers).encode())  # Send finger count to Arduino
                        
                        # Display the number of fingers on the screen
                        cv2.putText(img, f'{totalFingers}', (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6)

            # Show the webcam feed
            cv2.imshow("Webcam", img)

            # Exit the loop if ESC key is pressed
            if cv2.waitKey(5) & 0xff == 27:
                capture.release()
                cv2.destroyAllWindows()
                break

    if command == 'k':
        # Stop the red LED function (if it's active)
        arduino.write('k'.encode())

    if command == 's':
        # Start the finger pinching gesture program
        arduino.write('s'.encode())  # Notify Arduino to start finger pinch gesture

        # Camera setup for hand tracking
        width_cam, height_cam = 900, 600
        capture = cv2.VideoCapture(0)
        capture.set(3, width_cam)
        capture.set(4, height_cam)

        # Initialize MediaPipe hands detection
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpdraw = mp.solutions.drawing_utils
        tipIds = [4, 8, 12, 16, 20]

        while True:
            success, img = capture.read()  # Capture frame from webcam
            img = cv2.flip(img, 1)  # Flip image horizontally

            # Process the image with MediaPipe
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            lmList = []  # List to store landmark coordinates

            if results.multi_hand_landmarks:
                # Iterate through detected hands
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                        mpdraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                    # Pinch gesture logic
                    if len(lmList) > 9:
                        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb coordinates
                        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger coordinates
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center of the pinch

                        # Draw landmarks and lines for visualization
                        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)
                        cv2.circle(img, (cx, cy), 5, (0, 0, 0), cv2.FILLED)

                        # Calculate distance between thumb and index finger
                        length = math.hypot(x2 - x1, y2 - y1)
                        volume(length)  # Adjust volume based on pinch distance

                        # Highlight the pinch point with color based on distance
                        if length < 50:
                            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)  # Red for small distance
                        if length > 200:
                            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)  # Green for large distance

            # Show the webcam feed
            cv2.imshow("Webcam", img)

            # Exit the loop if ESC key is pressed
            if cv2.waitKey(5) & 0xff == 27:
                capture.release()
                cv2.destroyAllWindows()
                break

    if command == 'a':
        # Stop the buzzer volume function (if it's active)
        arduino.write('a'.encode())

    if command == 't':
        # Read and display temperature from the sensor connected to Arduino
        arduino.write('t'.encode())
        time.sleep(0.1)
        temp = arduino.readline()  # Read temperature data from Arduino
        string = temp.decode('utf-8')  # Decode byte data to string
        print(string)

    if command == 'r':
        # Continue (no action, just prompt user again)
        continue

    if command == 'b':
        # Read and display light sensor data from Arduino
        arduino.write('b'.encode())
        time.sleep(0.1)
        light = arduino.readline()  # Read light sensor data from Arduino
        string2 = light.decode('utf-8')  # Decode byte data to string
        print(string2)

    if command == 'v':
        # Continue (no action, just prompt user again)
        continue
