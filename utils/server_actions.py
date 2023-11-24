def register_user(clients, client_socket, client_name, portas_possiveis):
    if not is_user_registered(client_name, clients):
        client_port = portas_possiveis[len(portas_possiveis) - 1]
        clients[client_socket] = {"Nome": client_name, "Porta": client_port}
        ip_usuario = client_socket.getpeername()[0]
        print(f"Novo usuário registrado: Nome={client_name}, Porta={client_port}, IP={ip_usuario}")
        return client_port, clients[client_socket]


def is_user_registered(client_name, clients):
    for key, value in clients.items():
        if value.get['Nome'] == client_name:
            return True
    return False
