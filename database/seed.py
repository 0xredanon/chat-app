import sqlite3
import hashlib
import os

def seed_db():
    """Seed the database with an initial admin user."""
    db_path = os.path.join(os.path.dirname(__file__), "../database/chat.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ("admin", admin_password, "admin"))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_db()