import socket
import pickle
import uuid
import threading
class GameServer:
    def __init__(self):
        self.entities = []
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.entities = []
        
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
                data = self.client_socket.recv(1024)

                received_object = pickle.loads(data)
                for e in received_object:
                    
                    self.entities.append(e)
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



class EntityToSend:
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.is_new = True
        self.is_mod = False
        self.color = color
        self.uuid = uuid.uuid4


