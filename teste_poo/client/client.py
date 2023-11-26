import socket
from utils.user_actions import UserActions


class Client:
    def __init__(self, server_address, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, server_port)
        self.porta_receber_chamadas = 0
        self.client_name = ''
        self.user_actions = UserActions(self.client_socket)

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def display_menu_and_return_option(self):
        print("Escolha uma opção:")
        print("1 - Registrar-se no servidor")
        print("2 - Realizar consulta de usuário")
        print("3 - Solicitar video chamada para um usuário")
        print("4 - Aguarda solicitação de videochamada")
        print("5 - Sair do servidor")

        choice = input("Opção: ")
        return choice

    def main(self):
        self.connect_to_server()

        while True:
            choice = self.display_menu_and_return_option()

            if choice == "1":
                porta_receber_chamadas, client_name = self.user_actions.request_register()
                if porta_receber_chamadas is None and client_name is None:
                    self.porta_receber_chamadas = porta_receber_chamadas
                    self.client_name = client_name
            elif choice == "2":
                response = self.user_actions.search_user()
                print(response)
            elif choice == "3":
                destination_name = input("Digite o nome do destinatário: ")
                user_response_accepted, user_ip_server_to_connect, user_port_server_to_connect = self.user_actions.request_video_call(destination_name)
                if user_response_accepted:
                    print("Video chamada aceita.")
                    ip_server_to_host_connection = self.client_socket.getsockname()[0]
                    port_server_to_host_connection = self.porta_receber_chamadas
                    self.user_actions.start_streaming(ip_server_to_host_connection, port_server_to_host_connection, user_ip_server_to_connect, user_port_server_to_connect)
            elif choice == "4":
                user_response_accepted, user_ip_server_to_connect, user_port_server_to_connect = self.user_actions.waiting_request_video_call(self.porta_receber_chamadas)
                if user_response_accepted:
                    print("Video chamada aceita.")
                    ip_server_to_host_connection = self.client_socket.getsockname()[0]
                    port_server_to_host_connection = self.porta_receber_chamadas
                    self.user_actions.start_streaming(ip_server_to_host_connection, port_server_to_host_connection, user_ip_server_to_connect, user_port_server_to_connect)
            elif choice == "5":
                unregister_success = self.user_actions.quit_server(self.client_name)
                if unregister_success:
                    self.client_socket.close()
                    break
                else:
                    continue


if __name__ == "__main__":
    client = Client("192.168.0.108", 7000)
    client.main()
