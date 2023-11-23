import socket
from vidstream import CameraClient
import cv2

def start_streaming(client_socket):
    print("Iniciando streaming.")

    ip, port = client_socket.getpeername()

    camera_client = CameraClient(ip, int(port))

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        # Display the frame
        cv2.imshow('Video Call', frame)
        if cv2.waitKey(1) == ord('q'):
            break




def main():
    # Criação do socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Endereço do servidor
    server_address = ("192.168.1.15", 7000)

    # Conecta ao servidor
    client_socket.connect(server_address)

    while True:
        response_from_server = client_socket.recv(4096).decode()
        if response_from_server:
            print(response_from_server)
            start_streaming(client_socket)

if __name__ == "__main__":
    main()