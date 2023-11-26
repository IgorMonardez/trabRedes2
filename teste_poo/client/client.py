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
                self.porta_receber_chamadas, _ = self.user_actions.request_register()
            elif choice == "2":
                response = self.user_actions.search_user()
                print(response)
            elif choice == "3":
                destination_name = input("Digite o nome do destinatário: ")
                self.user_actions.request_video_call(destination_name)
            elif choice == "4":
                self.user_actions.waiting_request_video_call(self.porta_receber_chamadas)
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
