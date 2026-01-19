import sqlite3
import json

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('bot_database.db')
    c = conn.cursor()
    
    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица заказов
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            items TEXT,
            total_price REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def save_cart(user_id, cart):
    """Сохранить корзину (упрощенно)"""
    with open(f'cart_{user_id}.json', 'w') as f:
        json.dump(cart, f)

def load_cart(user_id):
    """Загрузить корзину"""
    try:
        with open(f'cart_{user_id}.json', 'r') as f:
            return json.load(f)
    except:
        return {}