import socket
import pickle
import threading


# Configuración del servidor
host = "0.0.0.0"
port = 7173

# Inicializa el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

class GameServer:
    def __init__(self):
        self.entities=[]

game = GameServer()
class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

# Function to handle each client
def handle_client(client_socket):
    def send(what):
        data_to_send = what

        serialized_data = pickle.dumps(data_to_send)

        client_socket.send(serialized_data)

    def update():
        send(game)

    while True:
     # Receive the serialized data
        data = client_socket.recv(1024)

        if not data:
            break  # Connection closed

        # Deserializes the data to obtain the Python object
        received_object = pickle.loads(data)

        # Perform some operation with the received object
        print(f"Objeto recibido del cliente: {received_object.x}")
        game.entities.append({'x': received_object.x,'y':received_object.y,'width':100,'height':100})
        update()
    
    client_socket.close()
   
# Accept incoming connections and spawn a thread for each client
while True:
    client, addr = server_socket.accept()
    print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")

    # Create a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
        
