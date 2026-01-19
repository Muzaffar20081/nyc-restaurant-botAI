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
print(f"👑 Admin ID: {ADMIN_ID}")
print("=" * 50)

if not BOT_TOKEN or "ваш_токен" in BOT_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: Нет токена бота!")
    exit(1)

# Хранилище корзин
user_carts = {}

# ========== КОМАНДЫ ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"User {user.id} used /start")
    
    keyboard = [
        [InlineKeyboardButton("🍔 Бургеры", callback_data='burgers')],
        [InlineKeyboardButton("🍕 Пицца", callback_data='pizza')],
        [InlineKeyboardButton("🍣 Суши", callback_data='sushi')],
        [InlineKeyboardButton("🛒 Корзина", callback_data='cart')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')]
    ]
    
    await update.message.reply_text(
        f"🍽️ Привет, {user.first_name}!\n\n"
        "Добро пожаловать в *Food Delivery Bot*!\n"
        "Выберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "🤖 *Food Delivery Bot - Помощь*\n\n"
        "📋 *Доступные команды:*\n"
        "/start - Начать заказ\n"
        "/menu - Показать меню\n"
        "/help - Эта справка\n"
        "/status - Статус бота\n"
        "/admin - Админ панель\n\n"
        "🍽️ *Как заказать:*\n"
        "1. Нажмите /start\n"
        "2. Выберите категорию\n"
        "3. Добавьте блюда в корзину\n"
        "4. Перейдите в корзину\n\n"
        "📞 Поддержка: @Muzaffar20081"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /menu"""
    await start_command(update, context)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status"""
    users_count = len(user_carts)
    status_text = (
        "✅ *Статус бота:* Работает\n"
        "👥 *Пользователей онлайн:* {}\n"
        "🍽️ *Доступно блюд:* 9\n"
        "🕐 *Режим:* 24/7\n\n"
        "Бот готов к заказам! 🚀"
    ).format(users_count)
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /admin"""
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        users_count = len(user_carts)
        admin_text = (
            "👑 *Админ панель*\n\n"
            "📊 *Статистика:*\n"
            f"• Пользователей: {users_count}\n"
            f"• Ваш ID: {user_id}\n"
            f"• Токен: {BOT_TOKEN[:10]}...\n\n"
            "⚡ *Действия:*\n"
            "• /start - Тест бота\n"
            "• /status - Проверка\n"
            "• /help - Справка"
        )
        await update.message.reply_text(admin_text, parse_mode='Markdown')
    else:
        await update.message.reply_text("⛔ У вас нет доступа к админ панели!")

# ========== КНОПКИ ==========

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if user_id not in user_carts:
        user_carts[user_id] = {}
    
    if data == 'cart':
        await show_cart(query, user_id)
    elif data == 'help':
        await show_help(query)
    elif data == 'back':
        await show_main_menu(query)
    elif data in ['burgers', 'pizza', 'sushi']:
        await show_category(query, data)
    elif data.startswith('add_'):
        item = data[4:]  # Убираем 'add_'
        await add_to_cart(query, user_id, item)
    elif data == 'clear_cart':
        user_carts[user_id] = {}
        await query.edit_message_text("🗑️ Корзина очищена!")
    elif data == 'order':
        await query.edit_message_text("✅ Заказ оформлен! Скоро с вами свяжется оператор.")

async def show_cart(query, user_id):
    """Показать корзину"""
    cart = user_carts[user_id]
    
    if not cart:
        text = "🛒 *Ваша корзина пуста*\n\nДобавьте блюда из меню!"
    else:
        text = "🛒 *Ваша корзина:*\n\n"
        total = 0
        
        for item, qty in cart.items():
            price = 0
            for category in MENU.values():
                if item in category:
                    price = category[item]
                    break
            
            item_total = price * qty
            total += item_total
            text += f"• {item} ×{qty} = {item_total}₽\n"
        
        text += f"\n💵 *Итого: {total}₽*"
    
    keyboard = [
        [InlineKeyboardButton("✅ Оформить заказ", callback_data='order')],
        [InlineKeyboardButton("⬅️ Продолжить покупки", callback_data='back')],
        [InlineKeyboardButton("🗑️ Очистить корзину", callback_data='clear_cart')]
    ]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def show_category(query, category):
    """Показать категорию"""
    items = MENU[category]
    
    keyboard = []
    for name, price in items.items():
        keyboard.append([
            InlineKeyboardButton(f"{name} - {price}₽", callback_data=f"add_{name}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад", callback_data='back'),
        InlineKeyboardButton("🛒 Корзина", callback_data='cart')
    ])
    
    await query.edit_message_text(
        "*Выберите блюдо:*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def add_to_cart(query, user_id, item):
    """Добавить в корзину"""
    cart = user_carts[user_id]
    
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1
    
    # Находим цену
    price = 0
    for category in MENU.values():
        if item in category:
            price = category[item]
            break
    
    total_items = sum(cart.values())
    
    await query.edit_message_text(
        f"✅ *{item} добавлен в корзину!*\n\n"
        f"💰 Цена: {price}₽\n"
        f"🛒 Товаров в корзине: {total_items}\n\n"
        "*Продолжайте выбирать:*",
        parse_mode='Markdown'
    )

async def show_help(query):
    """Показать помощь в меню"""
    text = (
        "🤖 *Помощь по боту*\n\n"
        "• Выбирайте категории блюд\n"
        "• Добавляйте в корзину\n"
        "• Оформляйте заказ\n\n"
        "*Команды:*\n"
        "/start - начать заказ\n"
        "/menu - показать меню\n"
        "/help - эта справка\n\n"
        "📞 *Поддержка:* @Muzaffar20081"
    )
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
    
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def show_main_menu(query):
    """Показать главное меню"""
    keyboard = [
        [InlineKeyboardButton("🍔 Бургеры", callback_data='burgers')],
        [InlineKeyboardButton("🍕 Пицца", callback_data='pizza')],
        [InlineKeyboardButton("🍣 Суши", callback_data='sushi')],
        [InlineKeyboardButton("🛒 Корзина", callback_data='cart')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')]
    ]
    
    await query.edit_message_text(
        "🍽️ *Food Delivery Bot*\n\nВыберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ========== ЗАПУСК ==========

def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем команды
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("admin", admin_command))
    
    # Обработчик кнопок
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен! Доступные команды:")
    print("   /start - начать")
    print("   /menu - меню")
    print("   /help - помощь")
    print("   /status - статус")
    print("   /admin - админ")
    
    app.run_polling()

if __name__ == "__main__":
    main()
