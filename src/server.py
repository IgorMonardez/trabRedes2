import socket
import threading

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

# Inicializa a tabela dinâmica para armazenar informações dos clientes
clients = {}

# Função para lidar com cada cliente em threads separadas
def handle_client(client_socket):
    while True:
        client_data = client_socket.recv(1024).decode()
        if not client_data:
            break
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
        elif client_info[0] == "UNREGISTER":
            # Solicitação de desvinculação do servidor
            # Implemente a lógica para remover o cliente da tabela, se necessário
            print("Desvinculação do servidor solicitada.")
            client_socket.send("Desvinculação do servidor confirmada.".encode())
            break
        else:
            print("Mensagem inválida do cliente.")

    client_socket.close()


# Função para verificar se um usuário já está cadastrado
def is_user_registered(username):
    return username in clients

# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()
    #Inicia uma nova thread para cada cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
