from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

def general_menu():
    button_buy = KeyboardButton('Купити 💸')
    button_terms = KeyboardButton('Інформація ℹ️')
    button_ref_link = KeyboardButton('Рефералка 🔗')
    button_referrals = KeyboardButton('Запрошені друзі 👯‍♀️')
    button_questions = KeyboardButton('Кількість відповідей 🤓')
    button_get = KeyboardButton('Поставити запитання ❓')
    #adding everything in one line,so smaller button  size adjustment will include all buttons
    general_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_buy,button_terms,button_ref_link,button_referrals,button_questions,button_get)
    return general_menu_kb