import socket

# Crie um dicionário para armazenar informações dos clientes (nome e endereço de porta)
clientes = {}

# Crie um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Defina o endereço e a porta do servidor
server_address = ('localhost', 12345)

# Faça o servidor escutar na porta especificada
server_socket.bind(server_address)
server_socket.listen(5)

print("Servidor aguardando conexões...")

while True:
    # Aceite a conexão de um cliente
    client_socket, client_address = server_socket.accept()

    # Receba os dados do cliente
    data = client_socket.recv(1024).decode()

    # Divida os dados em partes
    parts = data.split()

    if parts[0] == 'REGISTRO':
        # Registre o cliente
        nome = parts[1]
        ip = parts[2]
        porta = parts[3]

        if nome not in clientes:
            clientes[nome] = (ip, porta)
            print(f"Novo usuário registrado: {nome} ({ip}:{porta})")
            client_socket.send("Registro realizado com sucesso.".encode())
        else:
            print(f"Usuário já registrado: {nome} ({ip}:{porta})")
            client_socket.send("Usuário já registrado.".encode())
    elif parts[0] == 'CONSULTA':
        # Consulta de endereço por nome de usuário
        nome = parts[1]
        if nome in clientes:
            endereco = f"Nome: {nome}, IP: {clientes[nome][0]}, Porta: {clientes[nome][1]}"
            client_socket.send(endereco.encode())
        else:
            client_socket.send("Usuário não encontrado.".encode())
    elif parts[0] == 'DESVINCULAR':
        # Desvincular cliente
        nome = parts[1]
        if nome in clientes:
            del clientes[nome]
            client_socket.send("Desvinculação realizada com sucesso.".encode())
        else:
            client_socket.send("Usuário não encontrado.".encode())

    # Feche o socket do cliente
    client_socket.close()
