import socket
import pickle
import threading

from entities.enemies import Enemy, EnemyFactory

from entities.entity import Entity


# Configuración del servidor
host = "0.0.0.0"
port = 7173

# Inicializa el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)


clients = []

def serialize(data):
    data_to_send = data
    return pickle.dumps(data_to_send)

class GameServer:

    def __init__(self):\
        
        self.entities=[]
        self.entities_recieved = []
        self.entities_to_send = []
        self.new_entity(EnemyFactory.create_enemy(self, "goblin", 200, 200))

    def new_entity(self,entity):
        entity.is_new = False
        
        self.entities_to_send.append(entity)
        self.entities.append(entity)
        self.update()
    
    def mod_entity(self,entity):
        for e in self.entities:
            if e.uuid == entity.uuid:
                e.x = entity.x
                e.y = entity.y
                e.width = entity.width
                e.height = entity.height
                e.color = entity.color
                e.is_mod = False
                e.is_new = entity.is_new
                e.hit_points = entity.hit_points
            else:
                print(f"Entidad no encontrada")
    
    def handle_recieved_entity(self, entity):
        if entity.is_new == True:
            self.new_entity(entity)
        elif entity.is_mod == True:
            self.mod_entity(entity)
    
    def update(self):
        print(clients)
        for c in clients:
            data = serialize(self.entities_to_send)
            c.send(data)
            print(f"Entidades enviadas")
        self.entities_to_send = [];

game = GameServer()



class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.uuid = uuid
# Function to handle each client
def handle_client(client_socket):

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
        game.handle_recieved_entity(received_object)
        
        
    
    clients.remove(client_socket)
    client_socket.close()
   
# Accept incoming connections and spawn a thread for each client
try:
    while True:
        client, addr = server_socket.accept()
        print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
        clients.append(client)
        # Create a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()
finally:
    for c in clients:
        c.close()
        
