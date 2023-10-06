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

# Envia informações de registro para o servidor
registration_data = f"{client_name},{client_port}"
client_socket.send(registration_data.encode())

# Fecha o socket do cliente
client_socket.close()
