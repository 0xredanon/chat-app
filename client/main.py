import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from gui import ChatGUI
from network import NetworkClient
from auth import AuthManager
from server.config import SERVER_HOST, SERVER_PORT
from tkinter import messagebox
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize authentication
    auth = AuthManager()
    user = auth.login_or_register()
    if not user:
        logging.error("Authentication failed: No user data returned")
        messagebox.showerror("Error", "Authentication failed. Please try again.")
        return

    # Start GUI
    root = tk.Tk()
    root.withdraw()  # Hide the root window until connection is established

    # Initialize network client
    client = None
    try:
        client = NetworkClient(SERVER_HOST, SERVER_PORT, user["username"])
        root.deiconify()  # Show the root window
        gui = ChatGUI(root, client)
        root.mainloop()
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
        messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
        root.destroy()

if __name__ == "__main__":
    main()