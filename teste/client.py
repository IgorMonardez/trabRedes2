import socket

from utils.user_actions import \
    request_register, start_streaming, search_user, quit_server, request_video_call, \
    waiting_request_video_call

porta_receber_chamadas = 0
client_name = ''

def display_menu_and_return_option():
    print("Escolha uma opção:")
    print("1 - Registrar-se no servidor")
    print("2 - Realizar consulta de usuário")
    print("3 - Solicitar video chamada para um usuário")
    print("4 - Aguarda solicitação de videochamada")
    print("5 - (provisório) Aguarda início de videochamada com outro usuário")
    print("6 - Sair do servidor")

    choice = input("Opção: ")
    return choice

def main():
    # Criação do socket do cliente
    global porta_receber_chamadas
    global client_name
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
            porta, name = request_register(client_socket)
            if not porta:
                print("Usuário já cadastrado.")
            else:
                # Registro foi bem sucedido
                # Armazena a porta para receber chamadas
                porta_receber_chamadas = porta
                client_name = name
        elif choice == "2":
            response = search_user(client_socket)
            print(response)
        elif choice == "3":
            # Solicita uma video chamada para um usuário
            user_to_call = input("Digite o nome do usuário que deseja chamar: ")
            user_response_accepted, user_ip_server_to_connect, user_port_server_to_connect = request_video_call(client_socket, user_to_call)
            if user_response_accepted:
                print("Video chamada aceita.")
                ip_server_to_host_connection = client_socket.getsockname()[0]
                port_server_to_host_connection = porta_receber_chamadas
                start_streaming(ip_server_to_host_connection, port_server_to_host_connection, user_ip_server_to_connect, user_port_server_to_connect)
        elif choice == "4":
            # Aguarda solicitação de video chamada
            user_response_accepted, user_ip_server_to_connect, user_port_server_to_connect = waiting_request_video_call(client_socket, porta_receber_chamadas)
            if user_response_accepted:
                print("Video chamada aceita.")
                ip_server_to_host_connection = client_socket.getsockname()[0]
                port_server_to_host_connection = porta_receber_chamadas
                start_streaming(ip_server_to_host_connection, port_server_to_host_connection, user_ip_server_to_connect, user_port_server_to_connect)
        # elif choice == "5":
        #     ip_receive_cam = client_socket.getsockname()[0]
        #     port_receive_cam = int(porta_receber_chamadas)
        #     start_streaming(client_socket, ip_receive_cam, port_receive_cam)
        elif choice == "6":
            unregister_success = quit_server(client_socket, client_name)
            if unregister_success:
                client_socket.close()
                break
            else:
                continue



if __name__ == "__main__":
    main()