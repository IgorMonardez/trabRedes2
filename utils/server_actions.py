def register_user(clients, client_socket, client_name, portas_possiveis):
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
    for key, value in clients.items():
        if value.get('Nome') == username:
            return f"IP={key}, Info: {value}"
    return None


def is_user_registered(client_name, clients):
    for client_socket, client_info in clients.items():
        if client_info['Nome'] == client_name:
            return True
    return False


def get_client_port_by_socket(client_socket, clients):
    for key, client_info in clients.items():
        if key == client_socket:
            return client_info['Porta']


def get_socket_by_ip(ip, clients):
    for client_socket, client_info in clients.items():
        socket_ip = client_socket.getsockname()[0]
        if socket_ip == ip:
            return client_socket
    return None
