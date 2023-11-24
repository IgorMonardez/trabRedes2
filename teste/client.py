import socket

from utils.user_actions import request_register, start_streaming, search_user

porta_receber_chamadas = 0

def display_menu_and_return_option():
    print("Escolha uma opção:")
    print("1 - Registrar-se no servidor")
    print("5 - Aguarda início de videochamada com outro usuário")

    choice = input("Opção: ")
    return choice

def main():
    # Criação do socket do cliente
    global porta_receber_chamadas
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Endereço do servidor
    server_address = ("192.168.1.15", 5000)

    # Conecta ao servidor
    client_socket.connect(server_address)

    while True:
        # Exibe um menu para o cliente escolher a ação que deseja realizar
        choice = display_menu_and_return_option()

        if choice == "1":
            # Se registra no servidor e recebe a porta para receber chamadas
            porta = request_register(client_socket)
            if not porta:
                print("Registro falhou.")
                client_socket.close()
            else:
                # Registro foi bem sucedido
                # Armazena a porta para receber chamadas
                porta_receber_chamadas = porta
        elif choice == "2":
            response = search_user(client_socket)
        elif choice == "5":
            ip_receive_cam = client_socket.getsockname()[0]
            port_receive_cam = int(porta_receber_chamadas)
            start_streaming(client_socket, ip_receive_cam, port_receive_cam)

if __name__ == "__main__":
    main()