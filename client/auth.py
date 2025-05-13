import sqlite3
import os
import hashlib
from tkinter import messagebox
import customtkinter as ctk
from server.db import init_db 

class AuthManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "../database/chat.db")
        # Initialize database and handle errors
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize database: {e}")
            raise

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(self, username, password):
        """Validate username and password inputs."""
        if not username or not password:
            return False
        if len(username) < 3 or len(username) > 32:
            return False
        if len(password) < 6:
            return False
        return True

    def get_db_connection(self):
        """Get database connection with context manager."""
        return sqlite3.connect(self.db_path)

    def login_or_register(self):
        """Create a login/register GUI and return authenticated user info."""
        root = ctk.CTk()
        root.title("Login / Register")
        root.geometry("300x250")

        user_data = {}

        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not self.validate_input(username, password):
                messagebox.showerror("Error", "Invalid username or password format")
                return
                
            hashed_password = self.hash_password(password)
            try:
                with self.get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                                 (username, hashed_password))
                    user = cursor.fetchone()
                    if user:
                        user_data["username"] = username
                        user_data["role"] = user[3]
                        root.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid credentials")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")
                root.destroy()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            
            if not self.validate_input(username, password):
                messagebox.showerror("Error", "Invalid username or password format")
                return
                
            hashed_password = self.hash_password(password)
            try:
                with self.get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                                 (username, hashed_password, "user"))
                    conn.commit()
                    messagebox.showinfo("Success", "Registered successfully!")
                    user_data["username"] = username
                    user_data["role"] = "user"
                    root.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"Database error: {e}")

        ctk.CTkLabel(root, text="Username").pack(pady=10)
        username_entry = ctk.CTkEntry(root)
        username_entry.pack(pady=5)
        ctk.CTkLabel(root, text="Password").pack(pady=10)
        password_entry = ctk.CTkEntry(root, show="*")
        password_entry.pack(pady=5)
        ctk.CTkButton(root, text="Login", command=login).pack(pady=10)
        ctk.CTkButton(root, text="Register", command=register).pack(pady=5)

        root.mainloop()
        return user_data if user_data else None