import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import socket
import threading
from handler import ClientHandler
from config import SERVER_HOST, SERVER_PORT

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(10)
        print(f"Server running on {SERVER_HOST}:{SERVER_PORT}...")
    except Exception as e:
        print(f"Failed to start server: {e}")
        return

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")
            threading.Thread(target=ClientHandler.handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()