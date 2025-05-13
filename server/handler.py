import sqlite3
from crypto import Crypto 
from client.utils import get_timestamp
import os
import socket
import select
import logging
from threading import Lock

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ClientHandler")

class ClientHandler:
    clients = []
    client_usernames = {}
    lock = Lock()

    @staticmethod
    def handle_client(client_socket, client_address):
        db_path = os.path.join(os.path.dirname(__file__), "../database/chat.db")
        username = None
        logger.info(f"New connection from {client_address}")
        try:
            client_socket.settimeout(60)
            
            # Authenticate client
            try:
                auth_message = client_socket.recv(1024).decode()
                logger.debug(f"Received auth message: {auth_message}")
            except Exception as e:
                logger.warning(f"Failed to receive auth message from {client_address}: {e}")
                return
                
            if auth_message.startswith("LOGIN:"):
                username = auth_message.split(":", 1)[1]
                
                try:
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
                        if not cursor.fetchone():
                            error_msg = "AUTH_FAILED"
                            client_socket.send(Crypto.encrypt_message(error_msg))
                            logger.warning(f"Authentication failed for {username}")
                            return
                except Exception as db_e:
                    logger.error(f"Database error during authentication: {db_e}")
                    client_socket.send(Crypto.encrypt_message("AUTH_ERROR"))
                    return
                    
                with ClientHandler.lock:
                    ClientHandler.client_usernames[client_socket] = username
                    ClientHandler.clients.append(client_socket)
                
                welcome = f"AUTH_SUCCESS:Welcome {username}! Connected users: {len(ClientHandler.clients)}"
                try:
                    client_socket.send(Crypto.encrypt_message(welcome))
                    logger.info(f"{username} authenticated successfully")
                except Exception as e:
                    logger.warning(f"Failed to send welcome message to {username}: {e}")
                    return

            else:
                client_socket.send(Crypto.encrypt_message("AUTH_REQUIRED"))
                logger.warning("Authentication message not received properly")
                return

            # Main message loop
            while True:
                try:
                    ready = select.select([client_socket], [], [], 1.0)
                    if ready[0]:
                        encrypted = client_socket.recv(4096)
                        if not encrypted:
                            raise ConnectionError("No data received - client disconnected")
                        
                        message = Crypto.decrypt_message(encrypted)
                        if message is None:
                            logger.warning(f"Failed to decrypt message from {username}")
                            continue
                        logger.debug(f"Received message from {username}: {message}")
                        if message.startswith("ADMIN:"):
                            ClientHandler.handle_admin_command(message, client_socket, username, db_path)
                        elif message == "PING":
                            logger.debug(f"Received PING from {username}")
                            client_socket.send(Crypto.encrypt_message("PONG"))
                        else:
                            ClientHandler.broadcast(message, client_socket, username, db_path)
                except socket.timeout:
                    continue
                except (ConnectionError, socket.error) as conn_e:
                    logger.info(f"Client {username} ({client_address}) disconnected: {conn_e}")
                    break
                except Exception as loop_e:
                    logger.error(f"Error in main loop for {username} ({client_address}): {loop_e}")
                    break
                    
        except Exception as e:
            logger.error(f"Error handling client {username or 'unknown'} ({client_address}): {e}")
        finally:
            with ClientHandler.lock:
                if client_socket in ClientHandler.clients:
                    ClientHandler.clients.remove(client_socket)
                if client_socket in ClientHandler.client_usernames:
                    del ClientHandler.client_usernames[client_socket]
            try:
                client_socket.close()
                logger.debug(f"Closed connection for {username or 'unknown'} ({client_address})")
            except Exception as close_e:
                logger.error(f"Error closing socket for {username or 'unknown'}: {close_e}")

    @staticmethod
    def broadcast(message, sender_socket, username, db_path):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)", 
                    (username, message, get_timestamp())
                )
                conn.commit()
                logger.debug("Message stored in database")
            
            encrypted_message = Crypto.encrypt_message(message)
            with ClientHandler.lock:
                disconnected_clients = []
                for client in ClientHandler.clients:
                    try:
                        client.send(encrypted_message)
                    except (ConnectionError, socket.error) as send_e:
                        logger.warning(f"Error sending to a client: {send_e}")
                        disconnected_clients.append(client)
                
                for client in disconnected_clients:
                    if client in ClientHandler.clients:
                        ClientHandler.clients.remove(client)
                    if client in ClientHandler.client_usernames:
                        del ClientHandler.client_usernames[client]
                    try:
                        client.close()
                    except Exception as close_e:
                        logger.error(f"Error closing disconnected client: {close_e}")
                    
        except Exception as e:
            logger.error(f"Error in broadcast: {e}")

    @staticmethod
    def handle_admin_command(message, client_socket, username, db_path):
        if username != "admin":
            client_socket.send(Crypto.encrypt_message("Unauthorized"))
            logger.warning(f"Unauthorized admin command request from {username}")
            return
        command = message.split(":", 1)[1]
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                if command == "GET_USERS":
                    cursor.execute("SELECT username FROM users")
                    users = [row[0] for row in cursor.fetchall()]
                    client_socket.send(Crypto.encrypt_message(",".join(users)))
                    logger.info("Admin requested user list")
                elif command == "CLEAR_CHAT":
                    cursor.execute("DELETE FROM messages")
                    conn.commit()
                    client_socket.send(Crypto.encrypt_message("Chat cleared"))
                    logger.info("Admin cleared chat history")
                else:
                    client_socket.send(Crypto.encrypt_message("Invalid admin command"))
                    logger.warning("Received unknown admin command")
        except Exception as e:
            logger.error(f"Error handling admin command: {e}")
            try:
                client_socket.send(Crypto.encrypt_message(f"Error: {e}"))
            except Exception as send_err:
                logger.error(f"Error sending admin error message: {send_err}")