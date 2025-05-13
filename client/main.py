import tkinter as tk
from gui import ChatGUI
from network import send_message, receive_message
import socket

# ایجاد سوکت برای اتصال به سرور
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))  # به سرور روی پورت 12345 متصل می‌شویم

# راه‌اندازی رابط گرافیکی چت
root = tk.Tk()
chat_gui = ChatGUI(root, client_socket)
root.mainloop()
