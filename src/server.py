import socket

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Inicializa a tabela dinâmica para armazenar informações dos clientes
clients = {}

# Função para verificar se um usuário já está cadastrado
def is_user_registered(username):
    return username in clients

# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()

    # Recebe o nome e a porta do cliente
    client_data = client_socket.recv(1024).decode()
    client_info = client_data.split(',')

    # Verifica o tipo de mensagem recebida
    if client_info[0] == "REGISTER":
        # Registro de novo usuário
        client_name, client_port = client_info[1], int(client_info[2])
        if not is_user_registered(client_name):
            clients[client_name] = (client_address[0], client_port)
            print(f"Novo usuário registrado: Nome={client_name}, IP={client_address[0]}, Porta={client_port}")
            client_socket.send("Registro bem-sucedido.".encode())
        else:
            print(f"Usuário {client_name} já está cadastrado.")
            client_socket.send("Usuário já cadastrado.".encode())
    elif client_info[0] == "QUERY":
        # Consulta de usuário
        user_to_query = client_info[1]
        if is_user_registered(user_to_query):
            user_info = clients[user_to_query]
            response = f"Nome={user_to_query}, IP={user_info[0]}, Porta={user_info[1]}"
            client_socket.send(response.encode())
        else:
            client_socket.send("Usuário não encontrado.".encode())


    # Fecha o socket do cliente
    client_socket.close()
