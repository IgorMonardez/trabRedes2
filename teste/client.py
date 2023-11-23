import pickle
import socket
import cv2
import numpy as np
import pyaudio
import struct

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.15', 7000))

# Open the webcam and start capturing video
cap = cv2.VideoCapture(0)

while True:
    # Capture a video frame
    ret, frame = cap.read()

    # Capture an audio frame
    # audio_frame = stream.read(1024)

    # Serialize the video and audio frames
    video_data = pickle.dumps(frame)
    print("Serialized a frame")

    # Send the length of the serialized video frame
    client_socket.sendall(struct.pack("L", len(video_data)))

    # Send the serialized video frame in chunks
    for i in range(0, len(video_data), 4096):
        client_socket.sendall(video_data[i:i + 4096])
        print("Sent a chunk of the frame")