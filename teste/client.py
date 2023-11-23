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

# Open the microphone and start capturing audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

while True:
    # Capture a video frame
    ret, frame = cap.read()

    # Capture an audio frame
    audio_frame = stream.read(1024)

    # Serialize the video and audio frames
    video_data = pickle.dumps(frame)
    audio_data = pickle.dumps(audio_frame)

    # Send the length of the serialized video frame
    client_socket.sendall(struct.pack("L", len(video_data)))

    # Send the serialized video frame in chunks
    for i in range(0, len(video_data), 4096):
        client_socket.sendall(video_data[i:i + 4096])

    # Send the length of the serialized audio frame
    client_socket.sendall(struct.pack("L", len(audio_data)))

    # Send the serialized audio frame in chunks
    for i in range(0, len(audio_data), 4096):
        client_socket.sendall(audio_data[i:i + 4096])