import tkinter as tk
from tkinter import scrolledtext
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from client.network import send_message
from utils import format_message

class ChatGUI:
    def __init__(self, master, client_socket):
        self.master = master
        self.master.title("Chat App")

        self.client_socket = client_socket

        # ایجاد فریم‌ها و اجزای گرافیکی
        self.chat_window = scrolledtext.ScrolledText(self.master, width=50, height=20)
        self.chat_window.grid(row=0, column=0, padx=10, pady=10)
        self.chat_window.config(state=tk.DISABLED)

        self.entry_box = tk.Entry(self.master, width=50)
        self.entry_box.grid(row=1, column=0, padx=10, pady=10)
        self.entry_box.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        message = self.entry_box.get()
        if message:
            # فرمت پیام و ارسال به سرور
            formatted_message = format_message("Client", message)
            send_message(self.client_socket, formatted_message)
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.insert(tk.END, f"You: {message}\n")
            self.chat_window.config(state=tk.DISABLED)
            self.entry_box.delete(0, tk.END)
