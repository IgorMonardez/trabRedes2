import socket
import threading
from vidstream import StreamingServer

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 7000)
server_socket.bind(server_address)

clients = []

def handle_client(client_socket):
    print("Conexão de cliente", client_address)
    client_socket.send("Conexão estabelecida".encode())
    clients.append(client_socket)

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