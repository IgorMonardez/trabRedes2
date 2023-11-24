import select
import socket
from vidstream import StreamingServer, CameraClient
import cv2

from utils.user_actions import request_register, aguardando_video_call

porta_receber_chamadas = 0

def send_video(ip_destino_cliente, porta_destino_cliente):
    camera = CameraClient(ip_destino_cliente, porta_destino_cliente)
    camera.start_stream()

def start_streaming(server_socket, ip, port):
    print("Iniciando streaming.")

    response = aguardando_video_call(server_socket)
    if response:
        ip_destino, port_destino = response.split(',')

        # Cliente espera receber a imagem do outro cliente
        print(f"Server para receber video via vidstream: {ip}, {port}")
        print(f"Server para enviar video via vidstream: {ip_destino}, {port_destino}")
        server = StreamingServer(ip, port)
        server.start_server()

        # Envia a imagem para o outro cliente
        send_video(ip_destino, int(port_destino))

def display_menu_and_return_option():
    print("Escolha uma opção:")
    print("1 - Registrar-se no servidor")
    print("5 - Recebe informação de outro cliente (Beta)")

    choice = input("Opção: ")
    return choice


def main():
    # Criação do socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Endereço do servidor
    server_address = ("192.168.1.15", 7000)

    # Conecta ao servidor
    client_socket.connect(server_address)

    while True:
        # Exibe um menu para o cliente escolher a ação que deseja realizar
        choice = display_menu_and_return_option()

        if choice == "1":
            # Se registra no servidor e recebe a porta para receber chamadas
            porta = request_register(client_socket)
            if not porta:
                print("Registro falhou.")
                client_socket.close()
            else:
                # Registro foi bem sucedido
                # Armazena a porta para receber chamadas
                porta_receber_chamadas = porta
        elif choice == "5":
            response_from_server = client_socket.recv(4096).decode().split(',')
            if response_from_server:
                print(response_from_server[0])
                ip_client = client_socket.getsockname()[0]
                port_client = int(response_from_server[1])
                # start_streaming(client_socket, ip_client, port_client)

        #
        # response_from_server = client_socket.recv(4096).decode().split(',')
        # if response_from_server:
        #     print(response_from_server[0])
        #     ip_client = client_socket.getsockname()[0]
        #     port_client = int(response_from_server[1])
        #     start_streaming(client_socket, ip_client, port_client)

if __name__ == "__main__":
    main()