import socket
import threading
import pickle
import struct
import cv2

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e porta do servidor
server_address = ('0.0.0.0', 7000)
server_socket.bind(server_address)

# Inicializa a tabela dinâmica para armazenar informações dos clientes
clients = {}
conexoes = {}
portas_possiveis = [7074, 7073, 7072, 7071, 7070]

# Função para lidar com cada cliente em threads separadas
def handle_client(client_socket):
    while True:
        # Caso padrão: Está chegando uma transmissão de vídeo, logo envio o video para o cliente de destino
        client_data = transmite_video(client_socket)

        if not client_data:
            break
        client_info = client_data.split(',')
        client_ip = client_address[0]
        if len(client_info) > 1 and client_info[1] is not None:
            client_name = client_info[1]
        else:
            client_name = ""
        # Verifica o tipo de mensagem recebida
        if client_info[0] == "REGISTER":
            # Registro de novo usuário
            client_port = portas_possiveis[len(portas_possiveis) - 1]

            if not is_user_registered(client_ip):
                clients[client_socket] = {"Nome": client_name, "Porta": client_port}
                print(f"Novo usuário registrado: Nome={client_name}, IP={client_ip}, Porta={client_port}")
                portas_possiveis.remove(client_port)
                client_socket.send("Registro bem sucedido.".encode())
                print(clients)
            else:
                print(f"Usuário {client_ip} já está cadastrado.")
                client_socket.send("Usuário já cadastrado.".encode())
        elif client_info[0] == "QUERY":
            # Consulta de usuário
            user_to_query = client_info[1]
            user_info = query_user_by_username(user_to_query)
            if user_info != "None":
                response = user_info
                client_socket.send(response.encode())
            else:
                client_socket.send("Usuário não encontrado.".encode())
        elif client_info[0] == "UNREGISTER":
            # Solicitação de desvinculação do servidor
            client_name = client_info[1]
            user_to_remove = query_user_socket(client_name)
            if user_to_remove == 0:
                print("Usuário não registrado no servidor.")
                client_socket.send("Usuário não registrado no servidor".encode())
            else:
                portas_possiveis.append(clients.get(user_to_remove)['Porta'])
                clients.pop(user_to_remove)
                print("Usuário desvinculado com sucesso.")
                print(clients)
                client_socket.send("Usuário desvinculado com sucesso.".encode())
                client_socket.close()
        elif client_info[0] == "INVITE_REQUEST":
            # TODO Colocar uma verificação em que o usuário pode somente fazer isso se estiver registrado no servidor.
            # Tratamento de solicitação de videochamada
            destinario_nome = client_info[1].strip()

            if not is_user_connected_by_username(destinario_nome):
                client_socket.send("Usuário não encontrado.".encode())
            else:
                cliente_socket_destino = query_user_socket(destinario_nome)
                nome_cliente_origem = get_username_by_socket(client_socket)
                send_invite_to_client(cliente_socket_destino, nome_cliente_origem).split(',')

        elif client_info[0] == "RESPONSE_INVITE_REQUEST":
            resposta_usuario = client_info[1] # Essa resposta vem do destino da call
            nome_cliente_origem = client_info[2] # Aqui eu tenho a origem da call

            # Envia para a origem da call a resposta do destino da call + informação de destino IP e destino PORT
            cliente_socket_origem = query_user_socket(nome_cliente_origem)
            destino_ip, destino_port = client_socket.getpeername()

            msg_final = f"{resposta_usuario}, {destino_ip}, {destino_port}"
            cliente_socket_origem.send(resposta_usuario.encode())
        else:
            print("Mensagem inválida do cliente.")

def transmite_video(client_socket):
    data = b""
    payload_size = struct.calcsize('>L')

    while True:
        # Leia o tamanho da mensagem
        while len(data) < payload_size:
            data += client_socket.recv(4096)
            if data.startswith(b'REGISTER') or data.startswith(b'QUERY') or data.startswith(b'UNREGISTER') or data.startswith(b'INVITE_REQUEST') or data.startswith(b'RESPONSE_INVITE_REQUEST'):
                return data.decode()

        # Leia os dados da mensagem
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack('>L', packed_msg_size)[0]

        # Continue lendo os dados da mensagem até que todos os dados sejam lidos
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        # Descompacte os dados da mensagem e reconstrua o quadro
        frame_data = data[:msg_size]
        data = data[msg_size:]
        payload = pickle.loads(frame_data)

        username = payload["username"]
        frame = payload["frame"]

        # Exibe o quadro recebido
        cv2.imshow("Quadro no servidor", frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    # Libere os recursos
    cv2.destroyAllWindows()

def send_invite_to_client(client_destino, nome_cliente_origem):
    try:
        message = f"Solicitação de videochamada recebida, deseja aceitar a requisição? (s/n): -{nome_cliente_origem}"
        client_destino.send(message.encode())
    except Exception as e:
        print(e)


# Função para verificar se um usuário já está cadastrado
def is_user_registered(ip):
    return ip in clients

def is_user_connected_by_username(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return True
    return False

def query_user_by_username(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return f"IP={key}, Info: {value}"
    return "None"

def query_user_socket(username):
    for key, value in clients.items():
        if value.get('Nome') == username:
            return key
    return 0

def get_username_by_socket(client_socket):
    client_ip = client_socket.getpeername()[0]
    for key, value in clients.items():
        teste = key.getpeername()[0]
        if teste == client_ip:
            return value.get('Nome')
    return None

# Começa a ouvir por conexões
server_socket.listen(5)
print("Servidor de Videoconferência iniciado.")

while True:
    print("Aguardando conexões...")
    client_socket, client_address = server_socket.accept()
    #Inicia uma nova thread para cada cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
