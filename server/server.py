import socket
import threading
from handler import handle_client
from config import SERVER_HOST, SERVER_PORT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Server running on {SERVER_HOST}:{SERVER_PORT}...")

# تابعی برای مدیریت اتصال هر کلاینت
def start_server():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
