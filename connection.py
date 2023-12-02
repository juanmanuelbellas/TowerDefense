import socket
import pickle
import uuid
import threading


class GameServer:
    def __init__(self):
        self.entities = []


class Client:
    def __init__(self, host, port, clock):
        self.host = host
        self.port = port
        self.entities = []
        self.clock = clock

        self.received_game = GameServer()
# Inicializa el socket del cliente
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        # iniciar thread para recibir objetos
        recieve_thread = threading.Thread(target=self.listen)
        recieve_thread.daemon = True
        recieve_thread.start()

    def listen(self):
        while True:
            try:
                self.clock.tick(60)
                data = self.client_socket.recv(4096)
                received_object = pickle.loads(data)

                self.entities = received_object
                print(f"Entidad recibida")
            except Exception as e:
                print(f"Error al recibir objetos: {str(e)}")

    def send_entities(self, data):
        # Objeto Python que se enviará al servidor
        data_to_send = data
        # Serializa el objeto Python
        serialized_data = pickle.dumps(data_to_send)
        # Envía los datos serializados al servidor
        self.client_socket.send(serialized_data)

    # Cierra la conexión
    def close(self):
        self.client_socket.close()
