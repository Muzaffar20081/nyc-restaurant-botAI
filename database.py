# database.py
import sqlite3

def init_db():
    """Создать базу данных"""
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        name TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        total REAL,
        items TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, name):
    """Добавить пользователя"""
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", 
                   (user_id, name))
    conn.commit()
    conn.close()
