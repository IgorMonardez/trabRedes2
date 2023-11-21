import select
import socket
import cv2
import pickle
import struct
import threading

teste = {}

def start_video_call():
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    destination_ip = teste.keys()
    destination_port = teste.values()

    try:
        peer_socket.connect((destination_ip, destination_port))
        print("Conectado ao peer para uma video call.")

        # Start sending video frames to the peer
        send_video_thread = threading.Thread(target=send_video, args=(peer_socket,))
        send_video_thread.start()

        # Start receiving video frames from the peer
        receive_video_thread = threading.Thread(target=receive_video, args=(peer_socket,))
        receive_video_thread.start()

    except Exception as e:
        print(f"Error ao iniciar video call: {e}")

    finally:
        peer_socket.close()
        print("Video call finalizada.")

def send_video(peer_socket):
    # Inicia a captura de vídeo do cliente
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        data = pickle.dumps({"frame": frame})
        message_size = struct.pack(">L", len(data))
        peer_socket.sendall(message_size + data)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

def receive_video(peer_socket):
    try:
        while True:
            data = b""
            payload_size = struct.calcsize('>L')

            while len(data) < payload_size:
                data += peer_socket.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack('>L', packed_msg_size)[0]

            while len(data) < msg_size:
                data += peer_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            payload = pickle.loads(frame_data)

            received_frame = payload["frame"]
            cv2.imshow("Received Frame", received_frame)

            if cv2.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(f"Error receiving video frame from peer: {e}")

    finally:
        cv2.destroyAllWindows()

def send_invite_request(client_socket, client_name):
    try:
        message = f"INVITE_REQUEST, {client_name}"
        client_socket.send(message.encode())
        response_info = client_socket.recv(1024).decode().split(',')

        response = input(response_info)

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
                resposta_videochamada = input(resposta_servidor_mensagem).lower() # TODO: Colocar uma verificação para o usuário usar apenas 's' ou 'n' como input

                resposta_final = f"{resposta_servidor_cabeçalho},{resposta_videochamada},{resposta_servidor_nome_cliente_origem}"
                client_socket.send(resposta_final.encode())
                break
        else:
            if tempo_restante % intervalo == 0:
                print(f"{tempo_restante} segundos restantes...")
            tempo_restante -= 1

    print("Estado de aguardando solicitação de chamada encerrado!")
    if resposta_videochamada == 'n':
        return False
    else:
        return True

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
                start_video_call()
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
