from vidstream import StreamingServer
import threading

# Create a streaming server
server = StreamingServer('0.0.0.0', 9990)
server.start_server()

# The server is now running in a separate thread.
# The server will receive video from the clients and send it to all connected clients.