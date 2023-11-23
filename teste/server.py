from vidstream import StreamingServer
import threading

# Create a streaming server
server = StreamingServer('localhost', 9990)

# Start the server in a new thread
t1 = threading.Thread(target=server.start_server)
t1.start()

# The server is now running in a separate thread.
# The server will receive video from the clients and send it to all connected clients.