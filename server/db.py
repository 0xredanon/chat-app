import sqlite3

def create_db():
    conn = sqlite3.connect('chatroom.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (id INTEGER PRIMARY KEY, user TEXT, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()
