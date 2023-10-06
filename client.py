import socket

# Crie um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Defina o endereço e a porta do servidor
server_address = ('localhost', 12345)

# Conecte-se ao servidor
client_socket.connect(server_address)

while True:
    print("1 - Registrar\n2 - Consultar\n3 - Desvincular\n4 - Sair")
    escolha = input("Escolha a opção: ")

    if escolha == '1':
        nome = input("Nome: ")
        ip = input("IP: ")
        porta = input("Porta: ")
        mensagem = f"REGISTRO {nome} {ip} {porta}"
    elif escolha == '2':
        nome = input("Nome do usuário a ser consultado: ")
        mensagem = f"CONSULTA {nome}"
    elif escolha == '3':
        nome = input("Nome do usuário a ser desvinculado: ")
        mensagem = f"DESVINCULAR {nome}"
    elif escolha == '4':
        mensagem = "SAIR"
        client_socket.send(mensagem.encode())
        break
    else:
        print("Opção inválida. Tente novamente.")
        continue

    client_socket.send(mensagem.encode())
    response = client_socket.recv(1024).decode()
    print(response)

# Feche o socket do cliente
client_socket.close()
