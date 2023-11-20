import socket

def send_invite_request(client_socket, server_address, client_name):
    try:
        client_socket.connect(server_address)
        message = f"INVITE_REQUEST, {client_name}"
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()

        if response == "ACCEPTED":
            print("Chamada aceita. Inicie a videochamada.")
        elif response == "REJECTED":
            print("Chamada recusada pelo destinatário.")
        else:
            print("Resposta inválida do servidor.")

    except ConnectionRefusedError:
        print("Não foi possível conectar ao destino.")
    finally:
        client_socket.close()

def main():
    while True:
        # Criação do socket do cliente a cada iteração
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: Define o endereço e porta do servidor
        # TODO: IP ICREDESEMFIO - 10.10.11.102 - Notebook Caio
        server_address = ("192.168.0.114", 7000)

        # Conecta ao servidor
        client_socket.connect(server_address)

        # Exibe um menu para o cliente escolher a ação
        print("Escolha uma ação:")
        print("1. Registrar-se no servidor")
        print("2. Realizar consulta de usuário")
        print("3. Solicitar desvinculação do servidor")
        print("4. Solicitar videochamada")
        print("5. Sair")

        choice = input("Opção: ")

        if choice == "1":
            # Opção 1: Registrar-se no servidor
            registration_data = f"REGISTER,{client_name}"
            client_socket.send(registration_data.encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == "2":
            # Opção 2: Realizar consulta de usuário
            user_to_query = input("Digite o nome do usuário que deseja consultar: ")
            query_request = f"QUERY,{user_to_query}"
            client_socket.send(query_request.encode())
            response = client_socket.recv(1024).decode()
            print("Resposta do servidor:", response)
        elif choice == "3":
            # Opção 3: Solicitar desvinculação do servidor
            client_socket.send(f"UNREGISTER,{client_name}".encode())
            print("Desvinculação do servidor solicitada.")
            response = client_socket.recv(1024).decode()
            print(response)
            break
        elif choice == "4":
            # Opção 4: Solicitar videochamada
            destination_name = input("Digite o nome do usuário que deseja chamar: ")
            send_invite_request(client_socket, server_address, destination_name)
        elif choice == "5":
            # Opção 5: Sair
            break
        else:
            print("Opção inválida. Tente novamente.")

        # Fecha o socket do cliente após cada iteração
        client_socket.close()

if __name__ == "__main__":
    client_name = input("Digite o nome do cliente: ")
    main()
