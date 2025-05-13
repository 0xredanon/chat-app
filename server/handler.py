import sqlite3
from db import create_db

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from client.network import send_message, receive_message

# ایجاد دیتابیس در ابتدا
create_db()

def handle_client(client_socket):
    while True:
        message = receive_message(client_socket)
        if message:
            print(f"Received: {message}")
            # ارسال پیام به تمامی کاربران متصل
            send_message(client_socket, message)
        else:
            break
    client_socket.close()
