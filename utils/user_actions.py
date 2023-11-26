import select
import time

from vidstream import StreamingServer, CameraClient, AudioSender, AudioReceiver


def request_register(client_socket):
    '''
    Função que solicita o registro de um novo usuário no servidor

    Parâmetros:
    client_socket (socket): Socket do cliente

    Retorna:
    tupla: Uma tupla contendo o número da porta e o nome do cliente se o registro for bem-sucedido, caso contrário, Falso.
    '''
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
    '''
    Função que solicita ao servidor informações sobre um usuário

    Parâmetros:
    client_socket (socket): Socket do cliente

    Retorno:
    str: Uma string contendo as informações de resposta do servidor
    '''
    user_to_query = input("Digite o nome do usuário que deseja consultar: ")
    query_request = f"QUERY,{user_to_query}"
    client_socket.send(query_request.encode())
    response = client_socket.recv(1024).decode()
    return response


def quit_server(client_socket, client_name):
    '''
    Função que solicita ao servidor o desvinculo do cliente

    Parâmetros:
    client_socket (socket): Socket do cliente
    client_name (str): Nome do cliente

    Retorno:
    bool: True se o desvinculo for bem-sucedido, caso contrário, False
    '''
    query_quit = f"EXIT,{client_name}"
    client_socket.send(query_quit.encode())
    response = client_socket.recv(1024).decode()
    if response == "Erro ao desvincular usuário do servidor":
        return False
    else:
        return True


def waiting_request_video_call(client_socket, port_connect):
    '''
    Função que aguarda uma solicitação de videochamada de outro cliente

    Parâmetros:
    client_socket (socket): Socket do cliente
    port_connect (int): Porta do cliente

    Retorno:
    tupla: Uma tupla contendo um booleano indicando se a solicitação de chamada de vídeo foi aceita, o endereço IP e o número da porta do servidor ao qual se conectar.
    '''
    intervalo = 5
    tempo_restante = 30

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            request, request_client_name, request_client_ip, request_client_port = client_socket.recv(
                1024).decode().split(',')
            if request == "INVITE_REQUEST":
                request_response = input(
                    f"Você recebeu uma solicitação de videochamada de {request_client_name}. Pressione ENTER para aceitar ou digite 'n' para recusar.")
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
    '''
    Solicite uma videochamada para outro usuário.

    Parâmetros:
    client_socket (socket): O socket do cliente.
    destination_name (str): O nome do usuário a ser chamado.

    Retorna:
    tupla: Uma tupla contendo um booleano indicando se a solicitação de chamada de vídeo foi aceita, o endereço IP e o número da porta do servidor ao qual se conectar.
    '''
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


def send_video(ip_destino_cliente, porta_destino_cliente):
    """
    Comece a transmitir vídeo para outro usuário.

    Parâmetros:
    ip_destino_cliente (str): O endereço IP do usuário para o qual transmitir.
    porta_destino_cliente (int): O número da porta do usuário para a qual transmitir.
    """
    camera = CameraClient(ip_destino_cliente, porta_destino_cliente)
    camera.start_stream()

def send_audio(ip_destino_cliente, porta_destino_cliente):
    """
       Comece a transmitir áudio para outro usuário.

       Parâmetros:
       ip_destino_cliente (str): O endereço IP do usuário para o qual transmitir.
       porta_destino_cliente (int): O número da porta do usuário para a qual transmitir.
       """
    audio = AudioSender(ip_destino_cliente, porta_destino_cliente)
    audio.start_stream()


def start_streaming(ip_server_to_host_connection, port_server_to_host_connection, ip_server_to_connect,
                    port_server_to_connect):
    """
    Comece a transmitir vídeo e áudio para outro usuário.

    Parâmetros:
    ip_server_to_host_connection (str): O endereço IP do servidor para hospedar a conexão.
    port_server_to_host_connection (int): O número da porta do servidor para hospedar a conexão.
    ip_server_to_connect (str): O endereço IP do servidor ao qual se conectar.
    port_server_to_connect (int): O número da porta do servidor ao qual se conectar.
    """
    print("Iniciando streaming.")

    ip_server_host = ip_server_to_host_connection.strip()
    port_server_host = int(port_server_to_host_connection.strip())

    ip_server_to_send_video_and_audio = ip_server_to_connect.strip()
    port_server_to_send_video_and_audio = int(port_server_to_connect.strip())

    print(f"Server para receber video via vidstream: {ip_server_host}, {port_server_host}")
    print(f"Server para enviar video via vidstream: {ip_server_to_send_video_and_audio}, {port_server_to_send_video_and_audio}")
    server = StreamingServer(ip_server_host, port_server_host)
    server.start_server()

    server_audio = AudioReceiver(ip_server_host, port_server_host + 100)
    server_audio.start_server()

    time.sleep(3)

    # Envia a imagem para o outro cliente
    send_video(ip_server_to_send_video_and_audio, int(port_server_to_send_video_and_audio))

    # Envia o audio para o outro cliente
    send_audio(ip_server_to_send_video_and_audio, int(port_server_to_send_video_and_audio) + 100)
