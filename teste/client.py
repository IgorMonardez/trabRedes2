import select
import socket
from vidstream import CameraClient, StreamingServer
import cv2

def aguadando_video_call(server_socket):
    intervalo = 5
    tempo_restante = 20

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([server_socket], [], [], 1)  #  Espera por 1 segundo
        if ready:
            response = server_socket.recv(4096).decode()
            if response:
                return response
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    return None

def send_video(ip_destino_cliente, porta_destino_cliente):
    camera = CameraClient(ip_destino_cliente, porta_destino_cliente)
    camera.start_stream()

def start_streaming(server_socket, ip, port):
    print("Iniciando streaming.")

    response = aguadando_video_call(server_socket)
    if response:
        ip_destino, port_destino = response.split(',')

        # Cliente espera receber a imagem do outro cliente
        print(f"Server para receber video via vidstream: {ip}, {port}")
        server = StreamingServer(ip, port)
        server.start_server()
        #
        # # Envia a imagem para o outro cliente
        # send_video()

        # response = server_socket.recv(4096).decode()
        # print(response)


    # Mostra a câmera do cliente para ele mesmo
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
        response_from_server = client_socket.recv(4096).decode().split(',')
        if response_from_server:
            print(response_from_server[0])
            ip_client = client_socket.getsockname()[0]
            port_client = int(response_from_server[1])
            start_streaming(client_socket, ip_client, port_client)

if __name__ == "__main__":
    main()