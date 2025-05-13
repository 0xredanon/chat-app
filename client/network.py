import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import socket
from server.crypto import Crypto
from client.utils import get_timestamp
import time
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkClient:
    def __init__(self, host, port, username):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
            # Send login message to server
            logging.debug(f"Sending LOGIN message for {username}")
            self.socket.send(f"LOGIN:{username}".encode('utf-8'))
            # Retry receiving authentication response
            for attempt in range(3):
                response = self.receive_message()
                if response:
                    if response.startswith("AUTH_SUCCESS"):
                        logging.info(f"Connected: {response}")
                        return
                    elif response.startswith(("AUTH_FAILED", "AUTH_ERROR")):
                        raise Exception(f"Authentication failed: {response}")
                logging.debug(f"Authentication attempt {attempt + 1} failed: No valid response")
                time.sleep(0.2)  # Increased delay for stability
            raise Exception("Authentication failed: Unable to receive valid response from server after 3 attempts")
        except Exception as e:
            logging.error(f"[NetworkClient] Error connecting to server: {e}")
            self.socket.close()
            raise

    def send_message(self, message):
        try:
            if not message:
                return False
            formatted = f"[{get_timestamp()}] {self.username}: {message}"
            encrypted = Crypto.encrypt_message(formatted)
            self.socket.sendall(encrypted)
            return True
        except ConnectionError:
            logging.error("[NetworkClient] Connection to server lost")
            return False
        except Exception as e:
            logging.error(f"[NetworkClient] Error sending message: {e}")
            return False

    def receive_message(self):
        try:
            encrypted = self.socket.recv(4096)
            if encrypted:
                decrypted = Crypto.decrypt_message(encrypted)
                if decrypted is None:
                    logging.error("[NetworkClient] Failed to decrypt server message")
                    return None
                logging.debug(f"Received message: {decrypted}")
                return decrypted
            logging.debug("[NetworkClient] No data received")
            return None
        except socket.error as e:
            logging.error(f"[NetworkClient] Error receiving message: {e}")
            return None

    def get_users(self):
        self.send_message("ADMIN:GET_USERS")
        response = self.receive_message()
        return response.split(",") if response else []

    def clear_chat(self):
        self.send_message("ADMIN:CLEAR_CHAT")