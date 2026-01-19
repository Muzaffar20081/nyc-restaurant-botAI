import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: BOT_TOKEN не найден в Variables!")
    exit(1)

print("=" * 50)
print("🚀 БОТ ЗАПУСКАЕТСЯ...")
print(f"🤖 Токен: {BOT_TOKEN[:15]}...")
print("=" * 50)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"✅ Привет, {user.first_name}!\n\n"
        f"Бот работает! Твой ID: {user.id}\n\n"
        "Команды:\n"
        "/start - это сообщение\n"
        "/help - помощь\n"
        "/test - тест"
    )
    logger.info(f"Пользователь {user.id} использовал /start")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /help"""
    await update.message.reply_text(
        "🤖 Помощь:\n\n"
        "Это тестовый бот.\n"
        "Если видишь это сообщение - бот работает!\n\n"
        "Развернут на Railway 24/7"
    )

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /test"""
    await update.message.reply_text("✅ Тест пройден! Бот отвечает.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на любое сообщение"""
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main():
    """Запуск бота"""
    try:
        # Создаем приложение
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("test", test_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Запускаем
        logger.info("✅ Бот запущен и готов к работе!")
        print("✅ Бот запущен! Отправь /start в Telegram")
        
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")

if __name__ == "__main__":
    main()
