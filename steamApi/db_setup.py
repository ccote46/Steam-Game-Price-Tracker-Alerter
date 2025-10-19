import sqlite3

def setup():
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()

    # Create one table to hold user emails
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Second table will hold game and user data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            target_price TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    connection.commit()
    connection.close()
