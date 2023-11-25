import socket
import threading

from utils.server_actions import register_user, get_client_port_by_socket, get_socket_by_ip, query_user_by_username

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 5000)
server_socket.bind(server_address)

clients_list = {}

portas_possiveis = [7777, 6001, 6002, 6003, 6004, 6005, 6006]

portas_usadas = []

def receive_message_from_client(client_socket):
    try:
        client_data = client_socket.recv(4096)
        client_info = client_data.decode().split(',')
        client_action = client_info[0]
        client_action_helper = client_info[1]
        return client_action, client_action_helper
    except Exception as e:
        print(e)
        return False

def query_user_socket(clients, username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return key
    return 0

def unregister_client_from_server(client_name):
    # Checa se o usuário está no servidor
    user_to_remove = query_user_socket(clients_list, client_name)
    if user_to_remove == 0:
        client_socket.send(f"Erro ao desvincular usuário do servidor".encode())
        return False
    else:
        portas_possiveis.append(clients_list.get(user_to_remove)['Porta']) 
        client_socket.send(f"Usuário {client_name} desconectado com sucesso".encode())
        client_socket.close()
        clients_list.pop(user_to_remove)
        print("Usuário desvinculado com sucesso.")
        print(clients_list)
        return True

def handle_client(client_socket):
    print("Conexão de cliente", client_address)
    while True:
        message_from_client = receive_message_from_client(client_socket)
        if not message_from_client:
            print("Erro ao receber mensagem do cliente.")
            client_socket.close()
        else:
            client_action = message_from_client[0]
            if client_action == "REGISTER":
                client_name = message_from_client[1]
                # Registro de novo usuário
                client_port, cliente = register_user(clients_list, client_socket, client_name, portas_possiveis)
                if not cliente:
                    print("Registro falhou.")
                    client_socket.send("Usuário já cadastrado".encode())
                else:
                    header = "Registro bem sucedido."
                    clients_list[client_socket] = cliente
                    portas_usadas.append(client_port)
                    portas_possiveis.remove(client_port)

                    msg = f"{header},{client_port}"
                    client_socket.send(msg.encode())
            elif client_action == "QUERY":
                client_name = message_from_client[1]
                user_info = query_user_by_username(clients_list, client_name)
                if user_info is None:
                    msg = "Usuário não cadastrado"
                else:
                    msg = user_info
                client_socket.send(msg.encode())
            elif client_action == "EXIT":
                client_name = message_from_client[1]
                user_unregistered = unregister_client_from_server(client_name)
                if user_unregistered:
                    break


            # (BETA) No momento que 2 clientes estiverem registrados, o servidor irá enviar a informação de um para o outro
            if len(clients_list) == 2:
                client1_socket = list(clients_list.keys())[0]
                client2_socket = list(clients_list.keys())[1]

                client1_port = get_client_port_by_socket(client1_socket, clients_list)
                client2_port = get_client_port_by_socket(client2_socket, clients_list)

                # Envia a informação do cliente 1 para o cliente 2
                client1_ip = client1_socket.getpeername()[0]
                client2_socket.send(f"{client1_ip},{client1_port}".encode())

                # Envia a informação do cliente 2 para o cliente 1
                client2_ip = client2_socket.getpeername()[0]
                client1_socket.send(f"{client2_ip},{client2_port}".encode())

# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()
    print("Conexão de cliente", client_address)

    #Inicia uma nova thread para cada cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()