import sqlite3
import os
import logging
import hashlib

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def manual_init_db():
    """Manually initialize the database for debugging."""
    db_path = os.path.join(os.path.dirname(__file__), "chat.db")
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    if not os.path.exists(schema_path):
        logging.error(f"Schema file not found: {schema_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if not cursor.fetchone():
        logging.info("Creating schema...")
        with open(schema_path, "r") as f:
            cursor.executescript(f.read())
        conn.commit()
        logging.info("Schema created.")
        
        # Seed admin user
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                      ("admin", admin_password, "admin"))
        conn.commit()
        logging.info("Admin user seeded.")
    
    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    logging.info(f"Tables in database: {tables}")
    
    conn.close()

if __name__ == "__main__":
    manual_init_db()