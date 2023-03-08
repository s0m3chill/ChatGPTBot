from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_buy = KeyboardButton('Купити 💸')
button_terms = KeyboardButton('Інформація ℹ️')
button_ref_link = KeyboardButton('Рефералка 🔗')
button_referrals = KeyboardButton('Зареферені юзери 👯‍♀️')
button_questions = KeyboardButton('Кількість відповідей 🤓')

greet_kb = ReplyKeyboardMarkup().add(
    button_buy).add(button_terms).add(button_ref_link).add(button_referrals).add(button_questions)