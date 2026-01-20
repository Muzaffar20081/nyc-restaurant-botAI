# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """Главное меню"""
    buttons = [
        [InlineKeyboardButton(text="🍔 Бургеры", callback_data="menu_burgers"),
         InlineKeyboardButton(text="🍕 Пицца", callback_data="menu_pizza")],
        [InlineKeyboardButton(text="🍣 Суши", callback_data="menu_sushi"),
         InlineKeyboardButton(text="🥤 Напитки", callback_data="menu_drinks")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
         InlineKeyboardButton(text="ℹ️ О нас", callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_button():
    """Кнопка назад"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
