import socket
import pickle
import threading
import time

from entities.enemies import Enemy, EnemyFactory

from entities.entity import Entity


clients = []


def serialize(data):
    data_to_send = data
    return pickle.dumps(data_to_send)


class ConnectionServer:
    def __init__(self, host, port):
       # Configuración del servidor
        self.host = host
        self.port = port
        self.start_server()

    def start_server(self):
        # Inicializa el socket del servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)


class GameServer:

    def __init__(self):
        # self.time_started = time.time()
        self.entities = []
        self.entities_recieved = []
        self.entities_to_send = []
        self.new_entity(EnemyFactory.create_enemy("goblin", 200, 200))

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def collision_handler(self, entity1, entity2):
        self.remove_entity(entity1)
        self.remove_entity(entity2)
        print("Hay colision")

    def collision_checker(self):
        collision = False
        for entity1 in self.entities:
            for entity2 in self.entities:
                if entity1.uuid != entity2.uuid:
                    if (entity1.x < entity2.x + entity2.width and
                        entity1.x + entity1.width > entity2.x and
                        entity1.y < entity2.y + entity2.height and
                            entity1.y + entity1.height > entity2.y):
                        collision = True

            if collision:
                self.collision_handler(entity1, entity2)

    def new_entity(self, entity):
        entity.is_new = False

        self.entities_to_send.append(entity)
        self.entities.append(entity)
        self.update()

    def mod_entity(self, entity):
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

                print(f"Entidad modificada {entity.hit_points} {entity.uuid} ")
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
            # c.send(data)
            self.send_all_entities(c)
            print(f"Entidades enviadas")
        self.entities_to_send = []

    def send_all_entities(self, client):
        print(clients)
        data = serialize(self.entities)
        client.send(data)
        print(f"Todas las entidades enviadas")


game = GameServer()
connection = ConnectionServer(host="127.0.0.1", port=7173)
# Function to handle each client


def handle_client(client_socket):

    while True:
     # Receive the serialized data
        data = client_socket.recv(4096)

        if not data:
            break  # Connection closed

        # Deserializes the data to obtain the Python object
        received_object = pickle.loads(data)

        # Perform some operation with the received object
        print(f"Objeto recibido del cliente: {received_object}")
        game.handle_recieved_entity(received_object)
        game.collision_checker()

    clients.remove(client_socket)
    client_socket.close()


# Accept incoming connections and spawn a thread for each client
try:
    while True:
        client, addr = connection.server_socket.accept()
        print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
        clients.append(client)
        game.send_all_entities(client)
        # Create a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()
finally:
    for c in clients:
        c.close()
