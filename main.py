import sys
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import socket

# netstat -anb

# Scripts will be attached to the Manager object in Unity

# Screen size
WIDTH, HEIGHT = 1500, 720

# Set up webcam
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# Set up the detection module
detector = HandDetector(maxHands=1, detectionCon=0.8)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 56020  # Port to listen on (non-privileged ports are > 1023)

# Set up the communication between the unity and the python script
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port_address = (HOST, PORT)


# Check if the connection is established
try:
    sock.connect(server_port_address)
    print("Connected to Unity")
except socket.error as e:
    print(str(e))
    sys.exit(1)


def detection(_frame):
    hands, _frame = detector.findHands(_frame)
    # Landmark values: (x, y, z) coordinates of each landmark (* 21 - number of landmarks)
    # If hands are detected, draw the landmarks on the frame
    if hands:
        # Convert to numpy array
        landmark_list = np.array(hands[0]['lmList'])
        # Subtract HEIGHT from the y coordinate (Second column)
        landmark_list[:, 1] = HEIGHT - landmark_list[:, 1]
        # Flatten the list of lists of landmark coordinates
        landmark_list = landmark_list.flatten()
        # Convert to a normal array
        landmark_list = list(landmark_list)
        data = str(landmark_list).encode()  # Encode the data as bytes
        sock.sendto(data, server_port_address)

    return _frame


while True:
    # Get the frame from the webcam
    ret, frame = capture.read()
    # Flip the image horizontally (my camera is mirrored)
    frame = cv2.flip(frame, 1)
    frame = detection(frame)

    cv2.imshow("VideoFrame", frame)
    cv2.waitKey(1)

    # Close the window when the Q key is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Close the window when the ESC key is pressed.
    if cv2.waitKey(1) & 0xFF == 27:
        break
    # Close the window when the X button is pressed.
    if cv2.getWindowProperty('VideoFrame', cv2.WND_PROP_VISIBLE) < 1:
        break
