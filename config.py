# config.py - конфигурация бота
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN") or "ВАШ_ТОКЕН_ЗДЕСЬ"

# Настройки ресторана
RESTAURANT_NAME = "NYC Restaurant AI"
RESTAURANT_PHONE = "+1 (212) 555-AI00"
RESTAURANT_ADDRESS = "456 AI Avenue, New York, NY 10002"
RESTAURANT_EMAIL = "info@nyc-restaurant-ai.com"

# Настройки работы
OPENING_HOURS = {
    "monday": "10:00-23:00",
    "tuesday": "10:00-23:00", 
    "wednesday": "10:00-23:00",
    "thursday": "10:00-23:00",
    "friday": "10:00-00:00",
    "saturday": "11:00-00:00",
    "sunday": "11:00-22:00"
}

# Настройки доставки
DELIVERY_PRICE = 200
FREE_DELIVERY_MIN = 1000
MIN_ORDER_PRICE = 300

# Пути к файлам
DATABASE_PATH = "database.db"
LOGS_PATH = "logs/bot.log"

# Администраторы
ADMIN_IDS = [123456789]  # Замените на ваш ID

print(f"✅ Конфигурация загружена: {RESTAURANT_NAME}")