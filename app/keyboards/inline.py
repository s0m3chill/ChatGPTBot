from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

def confirm_menu():
    question_buttons = [types.InlineKeyboardButton(text="Підтверджую", callback_data="confirm_yes"),
        types.InlineKeyboardButton(text="Не підтверджую", callback_data="confirm_no")]
    question_menu_kb = types.InlineKeyboardMarkup(row_width=2)
    question_menu_kb.add(*question_buttons)
    return question_menu_kb

def select_price_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="3 (100грн)", callback_data="price_3_100"),
        InlineKeyboardButton(text="5 (150грн)", callback_data="price_5_150"),
        InlineKeyboardButton(text="10 (200грн)", callback_data="price_10_200"),
    )
    return keyboard

def confirm_payment_menu(price: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="Підтвердити", callback_data=f"confirm_{price}"),
        InlineKeyboardButton(text="Скасувати", callback_data="cancel"),
    )
    return keyboard