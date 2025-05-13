import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
from utils import format_message
import threading
import random
import string
import socket
from queue import Queue
import logging
from server.crypto import Crypto

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatGUI:
    def __init__(self, master, network_client):
        self.message_queue = Queue()
        self.master = master
        self.master.title("Secure Chat App")
        self.network_client = network_client
        self.session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.chat_display = ctk.CTkTextbox(self.frame, height=400, width=600, state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.frame, width=500, placeholder_text="Type your message...")
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        if self.network_client.username == "admin":
            self.admin_button = ctk.CTkButton(self.frame, text="Admin Panel", command=self.open_admin_panel)
            self.admin_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.running = True
        self.start_receiving()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.process_messages()
        self.check_connection_timer()

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if not message:
            return
        try:
            if len(message) > 1000:
                messagebox.showwarning("Warning", "Message too long (max 1000 characters)")
                return
            formatted_message = format_message(self.session_id, message)
            if self.network_client.send_message(formatted_message):
                self.entry.delete(0, "end")
            else:
                messagebox.showerror("Error", "Failed to send message")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            messagebox.showerror("Error", f"Failed to send message: {e}")
            self.master.after(0, self.on_closing)

    def display_message(self, message):
        try:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{message}\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.yview("end")
        except Exception as e:
            logging.error(f"Error displaying message: {e}")

    def start_receiving(self):
        def receive_loop():
            while self.running:
                try:
                    message = self.network_client.receive_message()
                    if message:
                        self.message_queue.put(message)
                    elif message is None:
                        self.master.after(0, lambda: messagebox.showerror("Error", "Connection closed by server"))
                        self.master.after(0, self.on_closing)
                        break
                except (ConnectionError, socket.error) as e:
                    self.master.after(0, lambda: messagebox.showerror("Error", f"Lost connection to server: {e}"))
                    self.master.after(0, self.on_closing)
                    break
                except Exception as e:
                    logging.error(f"Error receiving message: {e}")
                    self.master.after(0, self.on_closing)
                    break
        self.receive_thread = threading.Thread(target=receive_loop, daemon=True)
        self.receive_thread.start()

    def process_messages(self):
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                self.display_message(msg)
        except Exception as e:
            logging.error(f"Error processing messages: {e}")
        finally:
            if self.running:
                self.master.after(100, self.process_messages)

    def open_admin_panel(self):
        if self.network_client.username != "admin":
            messagebox.showerror("Error", "Unauthorized access")
            return
        try:
            admin_window = ctk.CTkToplevel(self.master)
            admin_window.title("Admin Panel")
            admin_window.geometry("400x300")
            admin_window.grab_set()
            ctk.CTkLabel(admin_window, text="Admin Tools").pack(pady=10)
            ctk.CTkButton(admin_window, text="View Users", command=self.view_users).pack(pady=5)
            ctk.CTkButton(admin_window, text="Clear Chat History", command=self.clear_chat).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open admin panel: {e}")

    def view_users(self):
        users = self.network_client.get_users()
        messagebox.showinfo("Users", "\n".join(users))

    def clear_chat(self):
        self.network_client.clear_chat()
        messagebox.showinfo("Success", "Chat history cleared.")

    def on_closing(self):
        self.running = False
        try:
            self.network_client.socket.close()
            self.master.destroy()
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
            self.master.destroy()

    def check_connection_timer(self):
        if not self.running:
            return
        try:
            self.network_client.socket.sendall(Crypto.encrypt_message("PING"))
            self.master.after(5000, self.check_connection_timer)
        except (ConnectionError, socket.error) as e:
            logging.error(f"Connection check failed: {e}")
            messagebox.showerror("Error", "Connection lost")
            self.on_closing()