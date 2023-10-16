import socket
import pickle

class Server:
    pass

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

# Inicializa el socket del cliente
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))


    def send(self, data):
        # Objeto Python que se enviará al servidor
        data_to_send = data
        # Serializa el objeto Python
        serialized_data = pickle.dumps(data_to_send)
        # Envía los datos serializados al servidor
        self.client_socket.send(serialized_data)

    # Cierra la conexión
    def close(self):
        self.client_socket.close()

