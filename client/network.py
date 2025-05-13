import socket

# تابعی برای ارسال پیام به سرور
def send_message(client_socket, message):
    try:
        client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

# تابعی برای دریافت پیام از سرور
def receive_message(client_socket):
    try:
        message = client_socket.recv(1024).decode('utf-8')
        return message
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None
