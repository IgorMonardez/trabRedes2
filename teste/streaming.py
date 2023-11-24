import socket
from vidstream import StreamingServer

server = StreamingServer('192.168.1.15', 9999)
server.start_server()