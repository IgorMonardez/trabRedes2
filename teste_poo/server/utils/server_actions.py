import socket
class ServerActions:
    def __init__(self, clients_list):
        self.clients_list = clients_list

    def receive_message_from_client(self, client_socket):
        try:
            client_data = client_socket.recv(4096)
            client_info = client_data.decode().split(',')
            client_action = client_info[0]
            client_action_helper = client_info[1]
            return client_action, client_action_helper
        except Exception as e:
            print(e)
            return False

    def register_user(self, client_socket, client_name):
        if not self.is_user_registered(client_name):
            client_port = self.get_available_port()
            self.clients_list[client_socket] = {"Nome": client_name, "Porta": client_port}
            ip_usuario = client_socket.getpeername()[0]
            print(f"Novo usuário registrado: Nome={client_name}, Porta={client_port}, IP={ip_usuario}")
            response_msg = f"Registro bem sucedido. Porta={client_port}"
            client_socket.send(response_msg.encode())
        else:
            print(f"Usuário {client_name} já está cadastrado")
            response_msg = "Usuário já cadastrado"
            client_socket.send(response_msg.encode())

    def query_user_by_username(self, client_socket, username):
        for key, value in self.clients_list.items():
            if value.get('Nome') == username:
                response_msg = f"IP={key}, Info: {value}"
                client_socket.send(response_msg.encode())
                return
        response_msg = "Usuário não cadastrado"
        client_socket.send(response_msg.encode())

    def handle_invite_request(self, client_socket, dest_username):
        dest_socket = self.get_user_socket_by_username(dest_username)
        sender_name = self.clients_list[client_socket]["Nome"]
        sender_ip = client_socket.getpeername()[0]
        sender_port = self.clients_list[client_socket]["Porta"]
        dest_socket.send(f"INVITE_REQUEST,{sender_name},{sender_ip},{sender_port}".encode())

    def handle_invite_response(self, client_socket, response_info):
        response_info_list = response_info.split('-')
        is_accepted = response_info_list[0]
        if is_accepted == "True":
            dest_ip, dest_port = response_info_list[1], response_info_list[2]
            client_socket.send(f"{is_accepted},{dest_ip},{dest_port}".encode())
        else:
            client_socket.send("False,,".encode())

    def unregister_client_from_server(self, client_socket, client_name):
        if self.is_user_registered(client_name):
            self.clients_list.pop(client_socket)
            client_socket.send(f"Usuário {client_name} desconectado com sucesso".encode())
            print(f"Usuário {client_name} desconectado com sucesso.")
            return True
        else:
            client_socket.send("Erro ao desvincular usuário do servidor".encode())
            return False

    def is_user_registered(self, client_name):
        for client_info in self.clients_list.values():
            if client_info['Nome'] == client_name:
                return True
        return False

    def get_available_port(self):
        # Cria um socket para encontrar uma porta disponível
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.bind(('127.0.0.1', 0))  # Vincula a uma porta aleatória disponível
        _, porta = temp_socket.getsockname()
        temp_socket.close()
        return porta

    def get_user_socket_by_username(self, username):
        for client_socket, client_info in self.clients_list.items():
            if client_info['Nome'] == username:
                return client_socket
        return None
