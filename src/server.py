import socket
import threading

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 7000)
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
                clients[client_ip] = {"Nome": client_name, "Porta": client_port}
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
            user_info = query_user(user_to_query)
            if user_info != "None":
                response = user_info
                client_socket.send(response.encode())
            else:
                client_socket.send("Usuário não encontrado.".encode())
        elif client_info[0] == "UNREGISTER":
            # Solicitação de desvinculação do servidor
            client_name = client_info[1]
            user_to_remove = query_user_adress(client_name)
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
                break
        elif client_info[0] == "INVITE_REQUEST":
            # Tratamento de solicitação de videochamada
            sender_name = query_user_adress(client_address[0])['Nome']
            destination_name = client_info[1]
            print(f"Recebido pedido de videochamada de {sender_name} para {destination_name}")


        else:
            print("Mensagem inválida do cliente.")

    client_socket.close()


def teste(client_socket, destination_name, message):
    try:
        sender_ip = query_user_adress(destination_name)
        sender_port = 0000
        sender_address = (sender_ip, sender_port)
        client_socket.connect(sender_address)
        client_socket.send(message.encode())
    except ConnectionRefusedError:
        print(f"Não foi possível notificar {destination_name} sobre a decisão da chamada.")
    finally:
        client_socket.close()


# Função para verificar se um usuário já está cadastrado
def is_user_registered(ip):
    return ip in clients

def query_user(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return f"IP={key}, Info: {value}"
    return "None"

def query_user_adress(username):
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
