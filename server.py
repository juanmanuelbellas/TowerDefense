import socket
import pickle
import threading
import time
import argparse

from threading import Event
from entities.enemies import Enemy, EnemyFactory
from entities.entity import Entity

class ConnectionServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.start_server()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

class GameServer:
    def __init__(self):
        self.shutdown_event = Event()
        self.clients = []

        self.entities = []
        self.entities.append(EnemyFactory.create_enemy("goblin", 200, 200))


    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def collision_handler(self, entity1, entity2):
        self.remove_entity(entity1)
        self.remove_entity(entity2)
        print("Hay colision")
        self.update()

    def collision_checker(self):
        for i, entity1 in enumerate(self.entities):
            for j, entity2 in enumerate(self.entities):
                if i != j:  # Avoid comparing the same entity
                    if (entity1.x < entity2.x + entity2.width and
                        entity1.x + entity1.width > entity2.x and
                        entity1.y < entity2.y + entity2.height and
                        entity1.y + entity1.height > entity2.y):
                        self.collision_handler(entity1, entity2)
    
    def handle_recieved_entity(self, entity):
        self.entities.append(entity)
        self.update()

    def update(self):
        print(self.clients)
        for c in self.clients:
            data = self.serialize(self.entities)
            self.send_all_entities(c, data)
            print(f"Entidades enviadas")

    def send_all_entities(self, client, data):
        print(self.clients)
        client.send(data)
        print(f"Todas las entidades enviadas")

    @staticmethod
    def serialize(data):
        data_to_send = data
        return pickle.dumps(data_to_send)

    @staticmethod
    def handle_client(client_socket, game):
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            received_object = pickle.loads(data)
            print(f"Objeto recibido del cliente: {received_object}")
            game.handle_recieved_entity(received_object)
            game.collision_checker()
        game.remove_client(client_socket)
        client_socket.close()

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def start(self, host="127.0.0.1", port=7173):
        while not self.shutdown_event.is_set():
            connection = ConnectionServer(host=host, port=port)

            try:
                while True:
                    client, addr = connection.server_socket.accept()
                    print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
                    self.clients.append(client)
                    self.send_all_entities(client, self.serialize(self.entities))
                    client_thread = threading.Thread(target=self.handle_client, args=(client, self))
                    client_thread.start()
            finally:
                for c in self.clients:
                    c.close()
    
    def stop(self):
        self.shutdown_event.set()

if __name__ == "__main__":
    game_server = GameServer()
    game_server.start()

