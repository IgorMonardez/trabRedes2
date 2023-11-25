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
    if server_response == "Usuário já cadastrado":
        return False
    else:
        server_message, client_port = server_response.split(',')
        print(server_message)
        return client_port, name

def search_user(client_socket):
    user_to_query = input("Digite o nome do usuário que deseja consultar: ")
    query_request = f"QUERY,{user_to_query}"
    client_socket.send(query_request.encode())
    response = client_socket.recv(1024).decode()
    return response

def quit_server(client_socket, client_name):
    query_quit = f"EXIT,{client_name}"
    client_socket.send(query_quit.encode())
    response = client_socket.recv(1024).decode()
    if response == "Erro ao desvincular usuário do servidor":
        return False
    else:
        return True

def waiting_request_video_call(client_socket, port_connect):
    intervalo = 5
    tempo_restante = 30

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            request, request_client_name, request_client_ip, request_client_port = client_socket.recv(1024).decode().split(',')
            if request == "INVITE_REQUEST":
                request_response = input(f"Você recebeu uma solicitação de videochamada de {request_client_name}. Pressione ENTER para aceitar ou digite 'n' para recusar.")
                request_header = "RESPONSE_INVITE_REQUEST"
                request_response_info_to_connect = "-"
                if request_response == "":
                    ip_connect = client_socket.getsockname()[0]
                    request_response_info_to_connect = f"{ip_connect}-{port_connect}"

                msg = f"{request_header},{request_response}-{request_response_info_to_connect}-{request_client_name}"
                client_socket.send(msg.encode())

                if request_response == "":
                    return True, request_client_ip, request_client_port
                else:
                    return False, None, None
            else:
                continue
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    print("Estado de aguardando solicitação de chamada encerrado!")
    return False, None, None

def request_video_call(client_socket, destination_name):
    try:
        # Envia a mensagem para o servidor de INVITE_REQUEST
        client_socket.send(f"INVITE_REQUEST,{destination_name}".encode())

        # Espera a mensagem do servidor contendo a resposta do cliente
        response = client_socket.recv(1024).decode().split(',')

        request_response_accepted = bool(response[0])
        if request_response_accepted:
            destination_ip = response[1]
            destination_port = response[2]
            return True, destination_ip, destination_port
        else:
            return False, None, None

    except Exception as e:
        print(e)
        return False



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


def start_streaming(ip_server_to_host_connection, port_server_to_host_connection, ip_server_to_connect, port_server_to_connect):
    print("Iniciando streaming.")

    ip_server_host = ip_server_to_host_connection.strip()
    port_server_host = int(port_server_to_host_connection.strip())

    ip_server_to_send_video = ip_server_to_connect.strip()
    port_server_to_send_video = int(port_server_to_connect.strip())

    print(f"Server para receber video via vidstream: {ip_server_host}, {port_server_host}")
    print(f"Server para enviar video via vidstream: {ip_server_to_send_video}, {port_server_to_send_video}")
    # server = StreamingServer(ip_server_to_host_connection, port_server_to_connect)
    # server.start_server()
    #
    # time.sleep(10)
    #
    # # Envia a imagem para o outro cliente
    # send_video(ip_server_to_connect, int(port_server_to_connect))
