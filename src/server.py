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
    client_name, client_port = client_data.split(',')

    # Verifica se o usuário já está cadastrado
    if is_user_registered(client_name):
        print(f"Usuário {client_name} já está cadastrado.")
        client_socket.send("Usuário já cadastrado.".encode())
    else:
        # Armazena informações do cliente na tabela dinâmica
        clients[client_name] = (client_address[0], int(client_port))

    # Imprime a mensagem de confirmação
    print(f"Novo usuário registrado: Nome={client_name}, IP={client_address[0]}, Porta={client_port}")

    # Fecha o socket do cliente
    client_socket.close()
