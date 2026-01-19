import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, MENU

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🚀 FOOD BOT STARTING...")
print(f"🤖 Token exists: {bool(BOT_TOKEN)}")
print(f"🤖 Token preview: {BOT_TOKEN[:10]}...")
print(f"👑 Admin ID: {ADMIN_ID}")
print("=" * 50)

if not BOT_TOKEN or BOT_TOKEN == "ваш_токен_здесь":
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: Нет токена бота!")
    print("❌ Добавь BOT_TOKEN в Variables на Railway!")
    exit(1)

# ... остальной код тот же ...
