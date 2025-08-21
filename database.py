# database.py
# here I handle the SQLite database to save user messages and bot replies

import sqlite3  # sqlite for a simple local database

DB_FILE = "chat_logs.db"  # this is the file where chats will be stored

def init_db():
    # create DB and table if it doesn't exist
    conn = sqlite3.connect(DB_FILE)  # connect to database
    c = conn.cursor()  # cursor to execute SQL commands
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # auto-increment ID
            user_message TEXT,                     # store user message
            bot_response TEXT,                     # store bot reply
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  # store time
        )
    ''')
    conn.commit()  # save changes
    conn.close()  # close connection

def log_conversation(user_message, bot_response):
    # here I save each conversation in the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversations (user_message, bot_response)
        VALUES (?, ?)
    ''', (user_message, bot_response))
    conn.commit()  # save the new record
    conn.close()  # close connection

if __name__ == "__main__":
    init_db()  # initialize DB if running this file directly
    print("Database initialized.")  # simple message to confirm
