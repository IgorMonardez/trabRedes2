import select
import time
from vidstream import StreamingServer, CameraClient, AudioSender, AudioReceiver

class UserActions:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def request_register(self):
        try:
            name = input("Digite seu nome: ")
            header = "REGISTER"
            msg = f"{header},{name}"

            self.client_socket.send(msg.encode())

            server_response = self.client_socket.recv(1024).decode()
            if server_response == "Usuário já cadastrado":
                print(server_response)
                return None, None
            else:
                server_message, client_port = server_response.split(',')
                print(server_message)
                return client_port, name
        except Exception as e:
            print(f"Error during registration: {e}")
            return None, None

    def search_user(self):
        try:
            user_to_query = input("Digite o nome do usuário que deseja consultar: ")
            query_request = f"QUERY,{user_to_query}"
            self.client_socket.send(query_request.encode())
            response = self.client_socket.recv(1024).decode()
            return response
        except Exception as e:
            print(f"Error during user search: {e}")
            return "Erro na consulta do usuário."

    def quit_server(self, client_name):
        try:
            query_quit = f"EXIT,{client_name}"
            self.client_socket.send(query_quit.encode())
            response = self.client_socket.recv(1024).decode()
            if response == "Erro ao desvincular usuário do servidor":
                return False
            else:
                return True
        except Exception as e:
            print(f"Error during server exit: {e}")
            return False

    def waiting_request_video_call(self, port_connect):
        try:
            intervalo = 5
            tempo_restante = 30

            print(f"Timer iniciado para {tempo_restante} segundos.")

            while tempo_restante > 0:
                ready, _, _ = select.select([self.client_socket], [], [], 1)  # Espera por 1 segundo
                if ready:
                    request, request_client_name, request_client_ip, request_client_port = self.client_socket.recv(
                        1024).decode().split(',')
                    if request == "INVITE_REQUEST":
                        request_response = input(
                            f"Você recebeu uma solicitação de videochamada de {request_client_name}. Pressione ENTER para aceitar ou digite 'n' para recusar.")
                        request_header = "RESPONSE_INVITE_REQUEST"
                        request_response_info_to_connect = "-"
                        if request_response == "":
                            ip_connect = self.client_socket.getsockname()[0]
                            request_response_info_to_connect = f"{ip_connect}-{port_connect}"

                        msg = f"{request_header},{request_response}-{request_response_info_to_connect}-{request_client_name}"
                        self.client_socket.send(msg.encode())

                        if request_response == "":
                            return True, request_client_ip, request_client_port
                        else:
                            return False, None, None
                    else:
                        continue
                else:
                    if tempo_restante % intervalo == 0:
                        print(f"{tempo_restante} segundos restantes...")
                    tempo_restante -= 1

            print("Estado de aguardando solicitação de chamada encerrado!")
            return False, None, None
        except Exception as e:
            print(f"Error during waiting for video call request: {e}")
            return False, None, None

    def request_video_call(self, destination_name):
        try:
            self.client_socket.send(f"INVITE_REQUEST,{destination_name}".encode())

            response = self.client_socket.recv(1024).decode().split(',')

            request_response_accepted = bool(response[0])
            if request_response_accepted:
                destination_ip = response[1]
                destination_port = response[2]
                return True, destination_ip, destination_port
            else:
                return False, None, None

        except Exception as e:
            print(f"Error during video call request: {e}")
            return False

    def send_video(self, ip_destino_cliente, porta_destino_cliente):
        try:
            camera = CameraClient(ip_destino_cliente, porta_destino_cliente)
            camera.start_stream()
        except Exception as e:
            print(f"Error during video streaming: {e}")

    def send_audio(self, ip_destino_cliente, porta_destino_cliente):
        try:
            audio = AudioSender(ip_destino_cliente, porta_destino_cliente)
            audio.start_stream()
        except Exception as e:
            print(f"Error during audio streaming: {e}")

    def start_streaming(self, ip_server_to_host_connection, port_server_to_host_connection, ip_server_to_connect,
                        port_server_to_connect):
        try:
            print("Iniciando streaming.")

            ip_server_host = ip_server_to_host_connection.strip()
            port_server_host = int(port_server_to_host_connection.strip())

            ip_server_to_send_video_and_audio = ip_server_to_connect.strip()
            port_server_to_send_video_and_audio = int(port_server_to_connect.strip())

            print(f"Server para receber video via vidstream: {ip_server_host}, {port_server_host}")
            print(f"Server para enviar video via vidstream: {ip_server_to_send_video_and_audio}, {port_server_to_send_video_and_audio}")

            server = StreamingServer(ip_server_host, port_server_host)
            server.start_server()

            server_audio = AudioReceiver(ip_server_host, port_server_host + 100)
            server_audio.start_server()

            time.sleep(3)

            # Envia a imagem para o outro cliente
            self.send_video(ip_server_to_send_video_and_audio, int(port_server_to_send_video_and_audio))

            # Envia o áudio para o outro cliente
            self.send_audio(ip_server_to_send_video_and_audio, int(port_server_to_send_video_and_audio) + 100)
        except Exception as e:
            print(f"Error during streaming initialization: {e}")
