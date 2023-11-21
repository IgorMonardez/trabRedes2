import select
import socket

def send_invite_request(client_socket, server_address, client_name):
    try:
        message = f"INVITE_REQUEST, {client_name}"
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()

        if response == "s":
            print("Chamada aceita. Inicie a videochamada.")
        elif response == "n":
            print("Chamada recusada pelo destinatário.")
        else:
            print(response)

    except ConnectionRefusedError:
        print("Não foi possível conectar ao destino.")

def aguardando_solicitação_videochamada(segundos, client_socket):
    intervalo = 5
    tempo_restante = segundos

    print(f"Timer iniciado para {segundos} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            resposta_servidor = client_socket.recv(1024).decode()
            if resposta_servidor:
                resposta_videochamada = input(resposta_servidor).lower()
                client_socket.send(resposta_videochamada.encode())
                break
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    print("Timer concluído!")

def main():
    # Criação do socket do cliente a cada iteração
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO: Define o endereço e porta do servidor
    # TODO: IP ICREDESEMFIO - 10.10.11.102 - Notebook Caio
    server_address = ("192.168.1.15", 5000)

    # Conecta ao servidor
    client_socket.connect(server_address)

    while True:
        # # Criação do socket do cliente a cada iteração
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Exibe um menu para o cliente escolher a ação
        print("Escolha uma ação:")
        print("1. Registrar-se no servidor")
        print("2. Realizar consulta de usuário")
        print("3. Solicitar desvinculação do servidor")
        print("4. Solicitar videochamada")
        print("5. Aguarda solicitação de videochamada")
        print("6. Sair")

        choice = input("Opção: ")

        if choice == "1":
            # Opção 1: Registrar-se no servidor
            registration_data = f"REGISTER,{client_name}"
            client_socket.send(registration_data.encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == "2":
            # Opção 2: Realizar consulta de usuário
            user_to_query = input("Digite o nome do usuário que deseja consultar: ")
            query_request = f"QUERY,{user_to_query}"
            client_socket.send(query_request.encode())
            response = client_socket.recv(1024).decode()
            print("Resposta do servidor:", response)
        elif choice == "3":
            # Opção 3: Solicitar desvinculação do servidor
            client_socket.send(f"UNREGISTER,{client_name}".encode())
            print("Desvinculação do servidor solicitada.")
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()

        elif choice == "4":
            # Opção 4: Solicitar videochamada
            destination_name = input("Digite o nome do usuário que deseja chamar: ")
            send_invite_request(client_socket, server_address, destination_name)
        elif choice == "5":
            # Opção 6: Aguarda solicitacao de video chamada
            aguardando_solicitação_videochamada(60, client_socket)
        elif choice == "6":
            # Opção 6: Sair
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    client_name = input("Digite o nome do cliente: ")
    main()
