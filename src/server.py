import socket
import threading

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 5000)
server_socket.bind(server_address)

# Inicializa a tabela dinâmica para armazenar informações dos clientes
clients = {}
portas_possiveis = [7074, 7073, 7072, 7071, 7070]

# Função para lidar com cada cliente em threads separadas
def handle_client(client_socket):
    while True:
        client_data = client_socket.recv(1024).decode()
        if not client_data:
            break
        client_info = client_data.split(',')
        client_ip = client_address[0]
        client_name = client_info[1]
        # Verifica o tipo de mensagem recebida
        if client_info[0] == "REGISTER":
            # Registro de novo usuário
            client_port = portas_possiveis[len(portas_possiveis) - 1]

            if not is_user_registered(client_ip):
                clients[client_socket] = {"Nome": client_name, "Porta": client_port}
                print(f"Novo usuário registrado: Nome={client_name}, IP={client_ip}, Porta={client_port}")
                portas_possiveis.remove(client_port)
                client_socket.send("Registro bem sucedido.".encode())
                print(clients)
            else:
                print(f"Usuário {client_ip} já está cadastrado.")
                client_socket.send("Usuário já cadastrado.".encode())
        elif client_info[0] == "QUERY":
            # Consulta de usuário
            user_to_query = client_info[1]
            user_info = query_user_by_username(user_to_query)
            if user_info != "None":
                response = user_info
                client_socket.send(response.encode())
            else:
                client_socket.send("Usuário não encontrado.".encode())
        elif client_info[0] == "UNREGISTER":
            # Solicitação de desvinculação do servidor
            client_name = client_info[1]
            user_to_remove = query_user_socket(client_name)
            if user_to_remove == 0:
                print("Usuário não registrado no servidor.")
                client_socket.send("Usuário não registrado no servidor".encode())
            else:
                portas_possiveis.append(clients.get(user_to_remove)['Porta'])
                clients.pop(user_to_remove)
                print("Usuário desvinculado com sucesso.")
                print(clients)
                client_socket.send("Usuário desvinculado com sucesso.".encode())
                client_socket.close()
        elif client_info[0] == "INVITE_REQUEST":
            # Tratamento de solicitação de videochamada
            destinario_nome = client_info[1].strip()

            if not is_user_connected_by_username(destinario_nome):
                client_socket.send("Usuário não encontrado.".encode())
            else:
                cliente_socket_destino = query_user_socket(destinario_nome)
                resposta_usuario = send_invite_to_client(cliente_socket_destino)
                client_socket.send(f"Resposta do usuário: {resposta_usuario}".encode())

            #print(f"Recebido pedido de videochamada de {remetente_name} para {destinario_nome}")
        else:
            print("Mensagem inválida do cliente.")

def send_invite_to_client(client_destino):
    try:
        message = "Solicitação de videochamada recebida, deseja aceitar a requisição? (s/n): "
        client_destino.send(message.encode())
        resposta_usuario = client_destino.recv(1024).decode()
        return resposta_usuario
    except Exception as e:
        print(e)


# Função para verificar se um usuário já está cadastrado
def is_user_registered(ip):
    return ip in clients

def is_user_connected_by_username(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return True
    return False

def query_user_by_username(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return f"IP={key}, Info: {value}"
    return "None"

def query_user_socket(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return key
    return 0

# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()
    #Inicia uma nova thread para cada cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
