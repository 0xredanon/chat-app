import sqlite3
import os, sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.seed import seed_db

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), "../database/chat.db")
    schema_path = os.path.join(os.path.dirname(__file__), "../database/schema.sql")
    
    if not os.path.exists(schema_path):
        logging.error(f"Schema file not found at: {schema_path}")
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    logging.debug(f"Connecting to database at: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            logging.info("Users table not found. Creating schema...")
            try:
                with open(schema_path, "r") as f:
                    cursor.executescript(f.read())
                conn.commit()
                logging.info("Database schema initialized successfully.")
                
                seed_db()
                logging.info("Database seeded with initial data.")
            except Exception as e:
                logging.error(f"Failed to initialize schema: {e}")
                raise
        else:
            logging.debug("Users table already exists. Skipping schema creation.")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        raise
    finally:
        conn.close()