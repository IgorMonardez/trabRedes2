# server.py
import socket
import threading
from utils.server_actions import ServerActions

class Server:
    def __init__(self, server_address, server_port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, server_port)
        self.clients_list = {}  # Use a thread-safe data structure, e.g., threading.Lock()
        self.server_actions = ServerActions(self.clients_list)

    def start_server(self):
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        print("Servidor de Videoconferência iniciado.")

        try:
            while True:
                print("Aguardando conexões...")
                client_socket, client_address = self.server_socket.accept()
                print("Conexão de cliente", client_address)

                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()

        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                message_from_client = self.server_actions.receive_message_from_client(client_socket)
                if not message_from_client:
                    print("Erro ao receber mensagem do cliente.")
                    break

                client_action, client_action_helper = message_from_client
                if client_action == "REGISTER":
                    self.server_actions.register_user(client_socket, client_action_helper)
                elif client_action == "QUERY":
                    self.server_actions.query_user_by_username(client_socket, client_action_helper)
                elif client_action == "INVITE_REQUEST":
                    self.server_actions.handle_invite_request(client_socket, client_action_helper)
                elif client_action == "RESPONSE_INVITE_REQUEST":
                    self.server_actions.handle_invite_response(client_socket, client_action_helper)
                elif client_action == "EXIT":
                    self.server_actions.unregister_client_from_server(client_socket, client_action_helper)
                    break

        finally:
            client_socket.close()

if __name__ == "__main__":
    server = Server("0.0.0.0", 7000)
    server.start_server()
