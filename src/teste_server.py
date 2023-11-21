import cv2
import socket
import pickle
import struct

# Server socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8888))
server_socket.listen(5)

# OpenCV video capture setup
cap = cv2.VideoCapture(0)

while True:
    client_socket, addr = server_socket.accept()

    if client_socket:
        while True:
            ret, frame = cap.read()
            data = pickle.dumps(frame)

            # Send the size of the serialized frame to the client
            client_socket.sendall(struct.pack('>L', len(data)))

            # Send the serialized frame
            client_socket.sendall(data)

            if cv2.waitKey(1) == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
