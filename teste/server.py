# server.py
from vidstream import StreamingServer
import threading

server = StreamingServer('localhost', 9999)

t = threading.Thread(target=server.start_server)
t.start()

while True:
    pass