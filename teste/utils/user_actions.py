import select


def request_register(client_socket):
    # Solicita o nome do usuário
    name = input("Digite seu nome: ")
    header = "REGISTER"
    msg = f"{header},{name}"

    client_socket.send(msg.encode())

    server_response = client_socket.recv(1024).decode()
    if not server_response:
        return False
    else:
        server_message, client_port = server_response.split(',')
        print(server_message)
        return client_port

def aguardando_video_call(client_socket):
    intervalo = 5
    tempo_restante = 20

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            response = client_socket.recv(4096).decode()
            if response:
                return response
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    return None
