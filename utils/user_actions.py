import select
import time

from vidstream import StreamingServer, CameraClient


def request_register(client_socket):
    # Solicita o nome do usuário
    name = input("Digite seu nome: ")
    header = "REGISTER"
    msg = f"{header},{name}"

    client_socket.send(msg.encode())

    server_response = client_socket.recv(1024).decode()
    if not server_response:
        return False
    else:
        server_message, client_port = server_response.split(',')
        print(server_message)
        return client_port


def aguardando_video_call(client_socket):
    intervalo = 5
    tempo_restante = 20

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            response = client_socket.recv(4096).decode()
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


def start_streaming(client_socket, ip, port):
    print("Iniciando streaming.")

    response = aguardando_video_call(client_socket)
    if response:
        ip_destino, port_destino = response.split(',')

        print(f"Server para receber video via vidstream: {ip}, {port}")
        print(f"Server para enviar video via vidstream: {ip_destino}, {port_destino}")
        server = StreamingServer(ip, port)
        server.start_server()

        time.sleep(10)

        # Envia a imagem para o outro cliente
        send_video(ip_destino, int(port_destino))
