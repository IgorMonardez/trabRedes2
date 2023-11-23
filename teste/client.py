# client.py
from vidstream import CameraClient
import threading

client = CameraClient('localhost', 9999)

t = threading.Thread(target=client.start_stream)
t.start()

while True:
    pass