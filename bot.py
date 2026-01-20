# bot.py - ПРОСТОЙ БОТ
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Получаем токен из Railway
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения!")
    print("✅ Добавьте BOT_TOKEN в Railway Variables")
    exit(1)

print(f"✅ Бот запускается с токеном: {TOKEN[:10]}...")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Простая команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"👋 Привет, {message.from_user.first_name}!\nЯ работаю на Railway! 🚀")

# Обработка всех сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы сказали: {message.text}")

# Запуск
async def main():
    print("🚀 Бот запущен на Railway!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
