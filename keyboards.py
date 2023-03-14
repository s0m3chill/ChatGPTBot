from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

button_buy = KeyboardButton('Купити 💸')
button_terms = KeyboardButton('Інформація ℹ️')
button_ref_link = KeyboardButton('Рефералка 🔗')
button_referrals = KeyboardButton('Запрошені друзі 👯‍♀️')
button_questions = KeyboardButton('Кількість відповідей 🤓')
button_get = KeyboardButton('Поставити запитання ❓')

#adding everything in one line,so smaller button  size adjustment will include all buttons
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_buy,button_terms,button_ref_link,button_referrals,button_questions,button_get)

# it works:-)
question_buttons = [types.InlineKeyboardButton(text="Підтверджую", callback_data="confirm_yes"),
        types.InlineKeyboardButton(text="Не підтверджую", callback_data="confirm_no")]
question_kb = types.InlineKeyboardMarkup(row_width=2)
question_kb.add(*question_buttons)