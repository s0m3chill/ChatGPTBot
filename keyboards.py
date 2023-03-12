from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

button_buy = KeyboardButton('Купити 💸')
button_terms = KeyboardButton('Інформація ℹ️')
button_ref_link = KeyboardButton('Рефералка 🔗')
button_referrals = KeyboardButton('Зареферені юзери 👯‍♀️')
button_questions = KeyboardButton('Кількість відповідей 🤓')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_buy)
greet_kb.add(button_terms)
greet_kb.add(button_ref_link)
greet_kb.add(button_referrals)
greet_kb.add(button_questions)

# it works:-)
question_buttons = [types.InlineKeyboardButton(text="Підтверджую", callback_data="confirm_yes"),
        types.InlineKeyboardButton(text="Не підтверджую", callback_data="confirm_no")]
question_kb = types.InlineKeyboardMarkup(row_width=2)
question_kb.add(*question_buttons)