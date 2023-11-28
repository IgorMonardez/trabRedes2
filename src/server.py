import socket
import threading

from utils.server_actions import \
    register_user, \
    get_client_port_by_socket, \
    query_user_by_username, \
    get_user_socket_by_username, \
    send_invite_request_to_client, \
    send_invite_response_to_client

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 5000)
server_socket.bind(server_address)

# Dicionário para armazenar os clientes conectados
clients_list = {}

# Lista das portas possíveis para os clientes hospedarem a transmissão de vídeo
portas_possiveis = [7777, 6001, 6002, 6003, 6004, 6005, 6006]

# Lista das portas que estão sendo usadas no momento
portas_usadas = []


def receive_message_from_client(client_socket):
    """
    Receba uma mensagem de um cliente.

    Parâmetros:
    client_socket (socket): O socket do cliente.

    Retorna:
    tupla: Uma tupla contendo a ação e o auxiliar do cliente se a mensagem for recebida com sucesso, caso contrário, False.
    """
    try:
        client_data = client_socket.recv(4096)
        client_info = client_data.decode().split(',')
        client_action = client_info[0]
        client_action_helper = client_info[1]
        return client_action, client_action_helper
    except Exception as e:
        print(e)
        return False


def unregister_client_from_server(client_name):
    """
    Cancele o registro de um cliente do servidor.

    Parâmetros:
    client_name (str): O nome do cliente cujo registro será cancelado.

    Retorna:
    bool: True se o cancelamento do registro for bem-sucedido, caso contrário, False.
    """
    # Checa se o usuário está no servidor
    user_to_remove = get_user_socket_by_username(clients_list, client_name)
    if user_to_remove == 0:
        client_socket.send(f"Erro ao desvincular usuário do servidor".encode())
        return False
    else:
        portas_possiveis.append(clients_list.get(user_to_remove)['Porta'])
        client_socket.send(f"Usuário {client_name} desconectado com sucesso".encode())
        client_socket.close()
        clients_list.pop(user_to_remove)
        print("Usuário desvinculado com sucesso.")
        print(clients_list)
        return True


def handle_client(client_socket):
    """
    Lidar com as ações de um cliente.

    Parâmetros:
    client_socket (socket): O socket do cliente.
    """

    print("Conexão de cliente", client_address)
    while True:
        message_from_client = receive_message_from_client(client_socket)
        if not message_from_client:
            print("Erro ao receber mensagem do cliente.")
            client_socket.close()
        else:
            client_action = message_from_client[0]
            if client_action == "REGISTER":
                client_name = message_from_client[1]
                # Registro de novo usuário
                client_port, cliente = register_user(clients_list, client_socket, client_name, portas_possiveis)
                if not cliente:
                    print("Registro falhou.")
                    client_socket.send("Usuário já cadastrado".encode())
                else:
                    header = "Registro bem sucedido."
                    clients_list[client_socket] = cliente
                    portas_usadas.append(client_port)
                    portas_possiveis.remove(client_port)

                    msg = f"{header},{client_port}"
                    client_socket.send(msg.encode())
            elif client_action == "QUERY":
                client_name = message_from_client[1]
                user_info = query_user_by_username(clients_list, client_name)
                if user_info is None:
                    msg = "Usuário não cadastrado"
                else:
                    msg = user_info
                client_socket.send(msg.encode())
            elif client_action == "INVITE_REQUEST":
                client_destinatario = message_from_client[1]
                client_destinatario_socket = get_user_socket_by_username(clients_list, client_destinatario)

                client_remetente_nome = clients_list.get(client_socket)['Nome']
                client_remetente_socket = get_user_socket_by_username(clients_list, client_remetente_nome)
                client_remetente_ip = client_remetente_socket.getpeername()[0]
                client_remetente_porta = get_client_port_by_socket(client_remetente_socket, clients_list)
                send_invite_request_to_client(client_destinatario_socket, client_remetente_nome, client_remetente_ip, client_remetente_porta)
            elif client_action == "RESPONSE_INVITE_REQUEST":
                client_response_invite_request = message_from_client[1].split('-')
                send_invite_response_to_client(client_response_invite_request, clients_list)
            elif client_action == "EXIT":
                client_name = message_from_client[1]
                user_unregistered = unregister_client_from_server(client_name)
                if user_unregistered:
                    break


# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()
    print("Conexão de cliente", client_address)

    # Inicia uma nova thread para cada cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
