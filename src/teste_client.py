import cv2
import socket
import pickle
import struct

# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.15', 8888))

data = b""
payload_size = struct.calcsize('>L')

while True:
    # Receive the size of the serialized frame
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack('>L', packed_msg_size)[0]

    # Receive the serialized frame
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize the frame and display it
    frame = pickle.loads(frame_data)
    cv2.imshow('Received Video', frame)

    if cv2.waitKey(1) == ord('q'):
        break

client_socket.close()
