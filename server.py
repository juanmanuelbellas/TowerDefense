import socket
import pickle
import threading
import time
import argparse
import pygame
import math

from entities.enemies import Enemy, EnemyFactory
from entities.entity import Entity


class Client:
    def __init__(self, connection):
        self.display_y = 0
        self.display_x = 0
        self.display_width = 800
        self.display_height = 600
        self.connection = connection
        self.entities_to_send = []

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
        self.clients = []

        self.clock = pygame.time.Clock()

        self.entities = []
        self.entities.append(EnemyFactory.create_enemy("goblin", 200, 200))

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def collision_handler(self, entity1, entity2):
        self.remove_entity(entity1)
        self.remove_entity(entity2)
        print("Hay colision")
    
    def calc_distance_between (self,A,B):
        distancia = math.sqrt(
            pow((A.c_x - B.c_x), 2)+pow((A.c_y - B.c_y), 2))
        return distancia

    def target_setter(self,entity1):
        potential_targets = []
        distances = []
        if len(self.entities) > 0:
            for entity2 in self.entities:
                if entity1.team != entity2.team:
                    potential_targets.append(entity2)
                    distances.append(self.calc_distance_between(entity1,entity2))
            if len(potential_targets) > 0:
                entity1.set_target(potential_targets[distances.index(min(distances))])
            else:
                entity1.set_no_target()

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

    def update_entities(self):
        for entity in self.entities:
            self.target_setter(entity)
            entity.update()
        self.collision_checker()
    
    def update(self):
        self.update_entities()
        for c in self.clients:
            data = self.serialize(self.entities)
            self.send_all_entities(c)
            
    
    def get_entities_in_view(self,client):
        result = []
        for e in self.entities:
            if (e.x < client.display_x + client.display_width and
                e.x + e.width > client.display_x and
                e.y < client.display_y + client.display_height and
                e.y + e.height > client.display_y):
                    result.append(e)
        return result

    def send_all_entities(self, client):
        client.entities_to_send = self.get_entities_in_view(client)
        data = self.serialize(client.entities_to_send)
        client.connection.send(data)
        print(f"Todas las entidades enviadas")

    @staticmethod
    def serialize(data):
        data_to_send = data
        return pickle.dumps(data_to_send)

    @staticmethod
    def handle_client(client_socket, game):
        while True:
            data = client_socket.recv(2048 * 128)
            
            if not data:
                break
            received_object = pickle.loads(data)
            print(f"Objeto recibido del cliente: {received_object}")
            game.handle_recieved_entity(received_object)
           
        game.remove_client(client_socket)
        client_socket.close()

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
    
    def game_loop(self):
        while True:
            self.update()
            self.clock.tick(60)


    def start(self, host="127.0.0.1", port=7173):
        connection = ConnectionServer(host=host, port=port)
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.start()
        try:
            while True:
                client, addr = connection.server_socket.accept()
                print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
                
                c = Client(client)
                self.clients.append(c)
                self.send_all_entities(c)

                client_thread = threading.Thread(target=self.handle_client, args=(client, self))
                client_thread.start()
                self.clock.tick(60)
        finally:
            for c in self.clients:
                c.connection.close()

if __name__ == "__main__":
    game_server = GameServer()
    game_server.start()

