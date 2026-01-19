import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN", "8422033699:AAEoLcJq-LrKD6Su9Vtg4sNDf0v7IL5XRus")

print("=" * 50)
print("🚀 БОТ ЗАПУСКАЕТСЯ...")
print(f"🤖 Токен: {BOT_TOKEN[:15]}...")
print("=" * 50)

def start(update: Update, context: CallbackContext):
    """Обработчик /start"""
    user = update.message.from_user
    update.message.reply_text(
        f"✅ Привет, {user.first_name}!\n\n"
        f"Твой ID: {user.id}\n"
        "Бот работает на Railway 24/7!\n\n"
        "Команды:\n"
        "/start - это сообщение\n"
        "/menu - меню\n"
        "/help - помощь"
    )
    logger.info(f"User {user.id} started bot")

def help_command(update: Update, context: CallbackContext):
    """Обработчик /help"""
    update.message.reply_text("🤖 Бот для заказа еды. Используй /menu")

def menu_command(update: Update, context: CallbackContext):
    """Обработчик /menu"""
    menu_text = (
        "🍽️ *Меню:*\n\n"
        "🍔 *Бургеры:*\n"
        "• Классический бургер - 350₽\n\n"
        "🍕 *Пицца:*\n"
        "• Маргарита - 550₽\n\n"
        "🍣 *Суши:*\n"
        "• Филадельфия - 700₽\n\n"
        "Отправьте /start для заказа"
    )
    update.message.reply_text(menu_text, parse_mode='Markdown')

def echo(update: Update, context: CallbackContext):
    """Ответ на сообщения"""
    update.message.reply_text(f"Вы написали: {update.message.text}")

def main():
    """Запуск бота"""
    if not BOT_TOKEN or "ваш_токен" in BOT_TOKEN:
        logger.error("❌ Нет токена бота!")
        return
    
    try:
        # Создаем updater
        updater = Updater(token=BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчики
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("menu", menu_command))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        
        # Запускаем бота
        logger.info("✅ Бот запущен!")
        print("✅ Бот запущен! Отправь /start в Telegram")
        
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        print(f"❌ ОШИБКА: {e}")

if __name__ == "__main__":
    main()
