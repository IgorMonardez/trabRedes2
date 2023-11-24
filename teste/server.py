import socket
import threading

from utils.server_actions import register_user, get_client_port_by_socket, get_socket_by_ip

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 5000)
server_socket.bind(server_address)

clients_list = {}

portas_possiveis = [7777, 6001, 6002, 6003, 6004, 6005, 6006]

portas_usadas = []

def receive_message_from_client(client_socket):
    client_data = client_socket.recv(4096)

    try:
        client_info = client_data.decode().split(',')
        client_action = client_info[0]
        client_action_helper = client_info[1]
        return client_action, client_action_helper
    except Exception as e:
        print(e)
        return False


def handle_client(client_socket):
    print("Conexão de cliente", client_address)

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
                client_socket.close()
            else:
                header = "Registro bem sucedido."
                clients_list[client_socket] = cliente
                portas_usadas.append(client_port)
                portas_possiveis.remove(client_port)

                msg = f"{header},{client_port}"
                client_socket.send(msg.encode())

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

    # if len(clients) == 2:
    #     client1 = clients[0]
    #     client2 = clients[1]
    #
    #     # Envia a informação do cliente 1 para o cliente 2
    #     client1_ip = client1.getpeername()[0]
    #     client1_port = portas_usadas[0]
    #     client2.send(f"{client1_ip},{client1_port}".encode())
    #
    #     # Envia a informação do cliente 2 para o cliente 1
    #     client2_ip = client2.getpeername()[0]
    #     client2_port = portas_usadas[1]
    #     client1.send(f"{client2_ip},{client2_port}".encode())

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