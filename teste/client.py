from vidstream import CameraClient
import threading

# Create a camera client
client = CameraClient('192.168.1.15', 9990)
client.start_stream()

# The client is now running in a separate thread.
# The client will capture video from the camera and send it to the server.