import pickle
import socket
import struct

import cv2
import threading

class StreamingClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self._configure()
        self.__running = False
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def get_frame(self):
        return None

    def _cleanup(self):
        cv2.destroyAllWindows()

    def __client_streaming(self):
        self.__client_socket.connect((self.__host, self.__port))
        while self.__running:
            frame = self.get_frame()
            result, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self.__client_socket.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False

        self._cleanup()

    def start_stream(self):
        if self.__running:
            print("Client is already streaming!")
        else:
            self.__running = True
            client_thread = threading.Thread(target=self.__client_streaming)
            client_thread.start()

    def stop_stream(self):

        if self.__running:
            self.__running = False
        else:
            print("Client not streaming!")


class CameraClient(StreamingClient):
    def __init__(self, host, port, x_res=1024, y_res=576):
        self.__x_res = x_res
        self.__y_res = y_res
        self.__camera = cv2.VideoCapture(0)
        super(CameraClient, self).__init__(host, port)

    def get_camera(self):
        return self.__camera

    def _configure(self):
        self.__camera.set(3, self.__x_res)
        self.__camera.set(4, self.__y_res)
        super(CameraClient, self)._configure()

    def get_frame(self):
        ret, frame = self.__camera.read()
        return frame

    def _cleanup(self):
        self.__camera.release()
        cv2.destroyAllWindows()