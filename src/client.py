import select
import socket
import cv2
import pickle
import struct
import threading

from vidstream import StreamingServer

def send_invite_request(client_socket, client_name):
    try:
        message = f"INVITE_REQUEST, {client_name}"
        client_socket.send(message.encode())
        response_info = client_socket.recv(1024).decode().split(',')

        response = response_info[0]
        destination_ip = response_info[1]
        destination_port = int(response_info[2])

        print(f"Server para receber video via vidstream: {destination_ip}, {destination_port}")

        if response == "s":
            print("Chamada aceita. Inicie a videochamada.")
            return True
        elif response == "n":
            print("Chamada recusada pelo destinatário.")
            return False
        else:
            print(response)
            return False

    except ConnectionRefusedError:
        print("Não foi possível conectar ao destino.")

def aguardando_solicitação_videochamada(segundos, client_socket):
    intervalo = 5
    tempo_restante = segundos

    print(f"Timer iniciado para {segundos} segundos.")

    resposta_videochamada = 'n'

    while tempo_restante > 0:
        ready, _, _ = select.select([client_socket], [], [], 1)  # Espera por 1 segundo
        if ready:
            resposta_servidor = client_socket.recv(1024).decode()
            if resposta_servidor:
                resposta_servidor_info = resposta_servidor.split('-')
                resposta_servidor_cabeçalho = "RESPONSE_INVITE_REQUEST"
                resposta_servidor_mensagem = resposta_servidor_info[0]
                resposta_servidor_nome_cliente_origem = resposta_servidor_info[1]
                resposta_ip = resposta_servidor_info[2]
                respota_porta = resposta_servidor_info[3]

                resposta_videochamada = input(resposta_servidor_mensagem).lower() # TODO: Colocar uma verificação para o usuário usar apenas 's' ou 'n' como input

                resposta_final = f"{resposta_servidor_cabeçalho},{resposta_videochamada},{resposta_servidor_nome_cliente_origem}"
                client_socket.send(resposta_final.encode())
                msg = f"{resposta_videochamada},{resposta_ip},{respota_porta}"
                return msg
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    print("Estado de aguardando solicitação de chamada encerrado!")
    return resposta_videochamada

def start_video_chamada(server_socket):
    intervalo = 5
    tempo_restante = 20

    print(f"Timer iniciado para {tempo_restante} segundos.")

    while tempo_restante > 0:
        ready, _, _ = select.select([server_socket], [], [], 1)  #  Espera por 1 segundo
        if ready:
            response = server_socket.recv(4096).decode()
            if response:
                return response
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    return None

def main():
    # Criação do socket do cliente a cada iteração
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO: Define o endereço e porta do servidor
    # TODO: IP ICREDESEMFIO - 10.10.11.102 - Notebook Caio
    server_address = ("192.168.1.15", 7000)

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
            transmitir_video = send_invite_request(client_socket, destination_name)
            if transmitir_video:
                response = start_video_chamada(client_socket)
        elif choice == "5":
            # Opção 6: Aguarda solicitacao de video chamada
            resposta_video_chamada = aguardando_solicitação_videochamada(60, client_socket).split('')
            if len(resposta_video_chamada) == 3:
                ip = resposta_video_chamada[1]
                porta = resposta_video_chamada[2]
                print(f"Server para enviar video via vidstream: {ip}, {porta}")

                print("Chamada aceita. Inicie a videochamada.")
                response = start_video_chamada(client_socket)

        elif choice == "6":
            # Opção 6: Sair
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    client_name = input("Digite o nome do cliente: ")
    main()
