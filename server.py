import socket
import pickle
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 1234

# Inicializa el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

# Function to handle each client
def handle_client(client_socket):
    while True:
        # Receive the serialized data
        data = client_socket.recv(1024)

        if not data:
            break  # Connection closed

        # Deserializes the data to obtain the Python object
        received_object = pickle.loads(data)

        # Perform some operation with the received object
        print(f"Objeto recibido del cliente: {received_object.x}")

    client_socket.close()

# Accept incoming connections and spawn a thread for each client
while True:
    client, addr = server_socket.accept()
    print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")

    # Create a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
        
