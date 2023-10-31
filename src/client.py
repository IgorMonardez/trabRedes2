import socket

# Nome do cliente e porta para receber chamadas
# Solicita ao usuário que insira seu nome
client_name = input("Digite o nome do cliente: ")

# Solicita ao usuário que insira a porta para receber chamadas
while True:
    # Criação do socket do cliente a cada iteração
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO: Define o endereço e porta do servidor - O endereço de IP vai variar de acordo com o endereço de IP de seu roteador
    # TODO: IP ICREDESEMFIO - 10.10.11.102 - Notebook Caio
    server_address = ("192.168.0.108", 7000)

    # Conecta ao servidor
    client_socket.connect(server_address)

    # Exibe um menu para o cliente escolher a ação
    print("Escolha uma ação:")
    print("1. Registrar-se no servidor")
    print("2. Realizar consulta de usuário")
    print("3. Solicitar desvinculação do servidor")
    print("4. Sair")

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
        # Opção 4: Sair
        break
    else:
        print("Opção inválida. Tente novamente.")

    # Fecha o socket do cliente após cada iteração
    client_socket.close()
