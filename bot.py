import os
import asyncio
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Важно для Railway логов!
)

logger = logging.getLogger(__name__)

# Получаем токен
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    logger.error("❌ BOT_TOKEN не найден!")
    logger.info("Добавьте BOT_TOKEN в Railway Variables")
    sys.exit(1)

logger.info(f"✅ Токен получен: {TOKEN[:10]}...")

async def main():
    """Основная функция запуска бота"""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import CommandStart
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    @dp.message(CommandStart())
    async def start_cmd(message: types.Message):
        await message.answer(f"👋 Привет, {message.from_user.first_name}!\nБот работает на Railway! 🚀")
    
    @dp.message()
    async def echo(message: types.Message):
        await message.answer(f"Вы написали: {message.text}")
    
    logger.info("🚀 Бот запускается...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    # Этот блок ВАЖЕН для Railway
    logger.info("=" * 50)
    logger.info("NYC Restaurant AI Bot запускается")
    logger.info("=" * 50)
    
    asyncio.run(main())
