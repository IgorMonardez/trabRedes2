from vidstream import CameraClient
import threading

# Create a camera client
client = CameraClient('localhost', 9990)

# Start the client in a new thread
t1 = threading.Thread(target=client.start_stream)
t1.start()

# The client is now running in a separate thread.
# The client will capture video from the camera and send it to the server.