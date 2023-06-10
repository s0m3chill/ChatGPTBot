from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

def confirm_menu():
    question_buttons = [types.InlineKeyboardButton(text="Підтверджую", callback_data="confirm_yes"),
        types.InlineKeyboardButton(text="Не підтверджую", callback_data="confirm_no")]
    question_menu_kb = types.InlineKeyboardMarkup(row_width=2)
    question_menu_kb.add(*question_buttons)
    return question_menu_kb