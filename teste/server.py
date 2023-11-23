import socket
import threading
from vidstream import StreamingServer

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 7000)
server_socket.bind(server_address)

clients = []

portas = [7007, 6001, 6002, 6003, 6004, 6005, 6006]

portas_usadas = []

def handle_client(client_socket):
    print("Conexão de cliente", client_address)
    porta = portas[len(portas) - 1]
    portas_usadas.append(porta)
    portas.remove(porta)
    client_socket.send(f"Conexão estabelecida, {porta}".encode())
    portas.pop(0)
    clients.append(client_socket)

    if len(clients) == 2:
        client1 = clients[0]
        client2 = clients[1]

        # Envia a informação do cliente 1 para o cliente 2
        client1_ip = client1.getpeername()[0]
        client1_port = portas_usadas[0]
        client2.send(f"{client1_ip},{client1_port}".encode())

        # Envia a informação do cliente 2 para o cliente 1
        client2_ip = client2.getpeername()[0]
        client2_port = portas_usadas[1]
        client1.send(f"{client2_ip},{client2_port}".encode())

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