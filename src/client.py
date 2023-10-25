import socket

# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('localhost', 12345)

# Nome do cliente e porta para receber chamadas
client_name = "Vasco"
client_port = 7777

# Conecta ao servidor
client_socket.connect(server_address)

while True:
    # Exibe um menu para o cliente escolher a ação
    print("Escolha uma ação:")
    print("1. Registrar-se no servidor")
    print("2. Realizar consulta de usuário")

    choice = input("Opção: ")

    if choice == "1":
        # Opção 1: Registrar-se no servidor
        registration_data = f"REGISTER,{client_name},{client_port}"
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
    else:
        print("Opção inválida. Tente novamente.")

# Fecha o socket do cliente
client_socket.close()
