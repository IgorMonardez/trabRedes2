def register_user(clients, client_socket, client_name, portas_possiveis):
    """
    Registre um novo usuário no servidor.

    Parâmetros:
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.
    client_socket (socket): O socket do cliente.
    client_name (str): O nome do cliente a ser cadastrado.
    portas_possiveis (lista): Uma lista de portas possíveis para os clientes usarem.

    Retorna:
    tupla: Uma tupla contendo a porta do cliente e informações se o registro for bem-sucedido, caso contrário, False.
    """
    if not is_user_registered(client_name, clients):
        client_port = portas_possiveis[len(portas_possiveis) - 1]
        clients[client_socket] = {"Nome": client_name, "Porta": client_port}
        ip_usuario = client_socket.getpeername()[0]
        print(f"Novo usuário registrado: Nome={client_name}, Porta={client_port}, IP={ip_usuario}")
        return client_port, clients[client_socket]
    else:
        print(f"Usuário {client_name} já está cadastrado")
        return False, False


def query_user_by_username(clients, username):
    """
    Consulte um usuário pelo nome de usuário.

    Parâmetros:
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.
    nome de usuário (str): O nome de usuário do usuário a ser consultado.

    Retorna:
    str: As informações do usuário se o usuário for encontrado, caso contrário, Nenhum.
    """
    for key, value in clients.items():
        if value.get('Nome') == username:
            return f"IP={key}, Info: {value}"
    return None


def is_user_registered(client_name, clients):
    """
    Verifique se um usuário está registrado.

    Parâmetros:
    client_name (str): O nome do usuário a ser verificado.
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.

    Retorna:
    bool: True se o usuário estiver registrado, caso contrário, False.
    """
    for client_socket, client_info in clients.items():
        if client_info['Nome'] == client_name:
            return True
    return False


def get_client_port_by_socket(client_socket, clients):
    """
    Obtenha a porta de um cliente pelo socket.

    Parâmetros:
    client_socket (socket): O socket do cliente.
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.

    Retorna:
    int: a porta do cliente.
    """
    for key, client_info in clients.items():
        if key == client_socket:
            return client_info['Porta']


def get_socket_by_ip(ip, clients):
    """
    Obtenha um socket pelo seu endereço IP.

    Parâmetros:
    ip (str): O endereço IP do socket a ser recuperado.
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.

    Retorna:
    socket: O socket se encontrado, caso contrário, Nenhum.
    """
    for client_socket, client_info in clients.items():
        socket_ip = client_socket.getsockname()[0]
        if socket_ip == ip:
            return client_socket
    return None


def get_user_socket_by_username(clients, username):
    """
    Obtenha o socket de um usuário pelo nome de usuário.

    Parâmetros:
    clientes (dict): Um dicionário contendo os clientes conectados ao servidor.
    nome de usuário (str): O nome de usuário do usuário cujo socket deve ser recuperado.

    Retorna:
    socket: O socket do usuário, se encontrado, caso contrário, 0.
    """
    for key, value in clients.items():
        if value.get('Nome') == username:
            return key
    return 0


def send_invite_request_to_client(client_socket_destinatario, client_remetente_nome, client_remetente_ip,
                                  client_remetente_port):
    # Envia a mensagem de requisição para o cliente destinatário da chamada
    client_socket_destinatario.send(
        f"INVITE_REQUEST, {client_remetente_nome}, {client_remetente_ip}, {client_remetente_port}".encode())


def send_invite_response_to_client(client_response_invite_request, clients_list):
    """
    Envie uma solicitação de convite a um cliente.

    Parâmetros:
    client_socket_destinatario (socket): O socket do destinatário.
    client_remetente_nome (str): O nome do remetente.
    client_remetente_ip (str): O endereço IP do remetente.
    client_remetente_port (int): A porta do remetente.
    """
    # Envia uma mensagem de requisição para o cliente destinatário da chamada
    client_response = client_response_invite_request[0]

    client_requested_ip = client_response_invite_request[1]
    client_requested_port = client_response_invite_request[2]
    client_request_name = client_response_invite_request[3].strip()  # Esse é o nome do cliente que requisitou a chamada
    client_request_socket = get_user_socket_by_username(clients_list, client_request_name)

    # Se o usuário aceitou, client_response será vazio (Ele pressionou ENTER)
    if client_response == "":
        # Envia a mensagem para o usuário com as informações para iniciar a videocall
        client_request_socket.send(f"True,{client_requested_ip},{client_requested_port}".encode())
    else:
        client_request_socket.send("False,,".encode())
