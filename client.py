import pygame
import socket
import pickle

# Configuración del cliente
host = 'tituela.servebeer.com'
port = 27960 

# Inicializa el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Objeto Python que se enviará al servidor
data_to_send = {"nombre": "Alice", "edad": 30}

# Serializa el objeto Python
serialized_data = pickle.dumps(data_to_send)

# Envía los datos serializados al servidor
client_socket.send(serialized_data)

while True:
    recived_data = client_socket.recv(1024)
    recived_object = pickle.loads(recived_data)
    print({recived_object})

# Cierra la conexión
client_socket.close()
