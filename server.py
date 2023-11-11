import socket
import pickle
import threading


# Configuración del servidor
host = "0.0.0.0"
port = 27960

# Inicializa el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

class EntityToSend:
    def _init_(self):
        self.x = 600
        self.y = 300
        self.uuid = uuid.uuid4

class GameServer:
    def __init__(self):
        self.entities=[]
        self.entities_recieved = []

game = GameServer()
class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.uuid = uuid

# Function to handle each client
def handle_client(client_socket):
    def send(what):
        data_to_send = what

        serialized_data = pickle.dumps(data_to_send)

        client_socket.send(serialized_data)

    def update():
        send(game.entities)

    def load_object(entities_recieved):
        for entity_recieved in game.entities_recieved:
            for entity in game.entities:
                if entity.uuid == entity_recieved.uuid:
                    entity.x = entity_recieved.x
                    entity.y = entity_recieved.y
                    entity.width = entity.width
                    entity.height = entity.height
                else:
                    game.entities.append(entity_recieved)
            
                     
    while True:
     # Receive the serialized data
        data = client_socket.recv(1024)

        if not data:
            break  # Connection closed

        # Deserializes the data to obtain the Python object
        received_object = pickle.loads(data)

        # Perform some operation with the received object
        print(f"Objeto recibido del cliente: {received_object}")
        game.entities_recieved.append(received_object)
        
        update()
    
    client_socket.close()
   
# Accept incoming connections and spawn a thread for each client
while True:
    client, addr = server_socket.accept()
    print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")

    # Create a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
        
