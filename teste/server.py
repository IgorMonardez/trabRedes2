import pickle
import socket
import threading
import cv2
import numpy as np
import pyaudio
import struct

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 7000))
server_socket.listen(5)

def handle_client(client_socket):
    try:
        while True:
            # Receive the length of the serialized frame
            data_len = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]

            # Receive the serialized frame in chunks
            data = b""
            while len(data) < data_len:
                packet = client_socket.recv(min(data_len - len(data), 4096))
                if not packet:
                    return None
                data += packet

            # Check if all data has been received
            if len(data) != data_len:
                print("Data not fully received. Waiting for more data...")
                continue

            # Deserialize the frame
            frame = pickle.loads(data)

            # Display the frame
            cv2.imshow('Received Video', frame)

            if cv2.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(f"Error while handling client: {e}")

    finally:
        cv2.destroyAllWindows()
        client_socket.close()
        print("Client handling finished.")

while True:
    # Accept a new client and handle it in a new thread
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()