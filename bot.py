# bot.py - ГЛАВНЫЙ ФАЙЛ
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

# Импорт наших модулей
from config import BOT_TOKEN, RESTAURANT_NAME, ADMIN_ID
from menu.burgers import burgers
from menu.pizza import pizza
from menu.sushi import sushi
from keyboards import main_menu, back_button
import database

# Настройка
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Корзины пользователей (временное хранение)
user_carts = {}

# ========== КОМАНДЫ ==========
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    """Команда /start"""
    # Добавляем пользователя в БД
    database.add_user(message.from_user.id, message.from_user.first_name)
    
    text = f"""
👋 Привет, {message.from_user.first_name}!

Добро пожаловать в {RESTAURANT_NAME}!

Выберите категорию:
"""
    await message.answer(text, reply_markup=main_menu())

@dp.message(Command("menu"))
async def menu_cmd(message: types.Message):
    """Команда /menu"""
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    """Команда /help"""
    text = """
🤖 Помощь:

/menu - открыть меню
/cart - показать корзину
/start - начать заново

Выберите блюда из меню, добавьте в корзину и оформите заказ!
"""
    await message.answer(text)

# ========== МЕНЮ ==========
@dp.callback_query(F.data == "menu_burgers")
async def show_burgers(callback: types.CallbackQuery):
    """Показать бургеры"""
    text = "🍔 БУРГЕРЫ:\n\n"
    for item in burgers:
        text += f"{item['name']} - {item['price']}₽\n"
    
    # Кнопки для добавления
    buttons = []
    for item in burgers:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"➕ {item['name']}",
                callback_data=f"add_burger_{item['id']}"
            )
        ])
    buttons.append([types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "menu_pizza")
async def show_pizza(callback: types.CallbackQuery):
    """Показать пиццу"""
    text = "🍕 ПИЦЦА:\n\n"
    for item in pizza:
        text += f"{item['name']} - {item['price']}₽\n"
    
    buttons = []
    for item in pizza:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"➕ {item['name']}",
                callback_data=f"add_pizza_{item['id']}"
            )
        ])
    buttons.append([types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "menu_sushi")
async def show_sushi(callback: types.CallbackQuery):
    """Показать суши"""
    text = "🍣 СУШИ:\n\n"
    for item in sushi:
        text += f"{item['name']} - {item['price']}₽\n"
    
    buttons = []
    for item in sushi:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"➕ {item['name']}",
                callback_data=f"add_sushi_{item['id']}"
            )
        ])
    buttons.append([types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "menu_drinks")
async def show_drinks(callback: types.CallbackQuery):
    """Показать напитки"""
    drinks = [
        {"id": "cola", "name": "🥤 Кола", "price": 150},
        {"id": "fanta", "name": "🥤 Фанта", "price": 150},
        {"id": "water", "name": "💧 Вода", "price": 100},
    ]
    
    text = "🥤 НАПИТКИ:\n\n"
    for item in drinks:
        text += f"{item['name']} - {item['price']}₽\n"
    
    buttons = []
    for item in drinks:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"➕ {item['name']}",
                callback_data=f"add_drink_{item['id']}"
            )
        ])
    buttons.append([types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

# ========== КОРЗИНА ==========
@dp.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: types.CallbackQuery):
    """Добавить в корзину"""
    user_id = callback.from_user.id
    
    # Создаем корзину если нет
    if user_id not in user_carts:
        user_carts[user_id] = []
    
    # Определяем что добавить
    parts = callback.data.split("_")
    category = parts[1]
    item_id = parts[2]
    
    # Ищем товар
    item = None
    if category == "burger":
        item = next((i for i in burgers if i["id"] == item_id), None)
    elif category == "pizza":
        item = next((i for i in pizza if i["id"] == item_id), None)
    elif category == "sushi":
        item = next((i for i in sushi if i["id"] == item_id), None)
    elif category == "drink":
        drinks = [
            {"id": "cola", "name": "🥤 Кола", "price": 150},
            {"id": "fanta", "name": "🥤 Фанта", "price": 150},
            {"id": "water", "name": "💧 Вода", "price": 100},
        ]
        item = next((i for i in drinks if i["id"] == item_id), None)
    
    if item:
        user_carts[user_id].append(item)
        await callback.answer(f"✅ {item['name']} добавлен!")
    else:
        await callback.answer("❌ Ошибка")

@dp.callback_query(F.data == "cart")
async def show_cart(callback: types.CallbackQuery):
    """Показать корзину"""
    user_id = callback.from_user.id
    cart = user_carts.get(user_id, [])
    
    if not cart:
        text = "🛒 Корзина пуста"
        keyboard = back_button()
    else:
        total = sum(item["price"] for item in cart)
        text = "🛒 Ваша корзина:\n\n"
        for item in cart:
            text += f"• {item['name']} - {item['price']}₽\n"
        text += f"\n💰 Итого: {total}₽"
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="✅ Оформить", callback_data="checkout")],
            [types.InlineKeyboardButton(text="🗑️ Очистить", callback_data="clear_cart")],
            [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "checkout")
async def checkout(callback: types.CallbackQuery):
    """Оформить заказ"""
    user_id = callback.from_user.id
    cart = user_carts.get(user_id, [])
    
    if not cart:
        await callback.answer("Корзина пуста")
        return
    
    total = sum(item["price"] for item in cart)
    
    # Сохраняем заказ (упрощенно)
    import sqlite3
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    
    # Преобразуем корзину в текст
    items_text = ", ".join([item["name"] for item in cart])
    cursor.execute("INSERT INTO orders (user_id, total, items) VALUES (?, ?, ?)",
                   (user_id, total, items_text))
    
    conn.commit()
    conn.close()
    
    # Уведомляем админа
    await bot.send_message(
        ADMIN_ID,
        f"🆕 Новый заказ!\n"
        f"👤 Пользователь: {user_id}\n"
        f"💰 Сумма: {total}₽\n"
        f"🍽️ Заказ: {items_text}"
    )
    
    # Очищаем корзину
    user_carts[user_id] = []
    
    text = f"✅ Заказ оформлен!\n\nСумма: {total}₽\n\nСпасибо за заказ!"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔄 Новый заказ", callback_data="back")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "clear_cart")
async def clear_cart_cmd(callback: types.CallbackQuery):
    """Очистить корзину"""
    user_id = callback.from_user.id
    if user_id in user_carts:
        user_carts[user_id] = []
    
    await callback.answer("Корзина очищена")
    await show_cart(callback)

# ========== ДРУГОЕ ==========
@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    """О ресторане"""
    from config import RESTAURANT_NAME, RESTAURANT_PHONE, RESTAURANT_ADDRESS
    
    text = f"""
🏪 {RESTAURANT_NAME}

📍 Адрес: {RESTAURANT_ADDRESS}
📞 Телефон: {RESTAURANT_PHONE}

🕐 Время работы:
Пн-Пт: 10:00 - 23:00
Сб-Вс: 11:00 - 00:00

🚚 Доставка: 30-60 минут
"""
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

@dp.callback_query(F.data == "back")
async def back_to_menu(callback: types.CallbackQuery):
    """Вернуться в меню"""
    await callback.message.edit_text("🏠 Главное меню:", reply_markup=main_menu())
    await callback.answer()

# ========== ЗАПУСК ==========
async def main():
    # Инициализируем БД
    database.init_db()
    
    print("=" * 50)
    print(f"🚀 Бот запускается...")
    print(f"👑 Админ: {ADMIN_ID}")
    print("=" * 50)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
