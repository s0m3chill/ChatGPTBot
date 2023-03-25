import config

from core import bot, DataStorage
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

buy_price = 0

async def select_price(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="3 (100uah)", callback_data="price_100"),
        InlineKeyboardButton(text="5 (150uah)", callback_data="price_150"),
        InlineKeyboardButton(text="10 (200uah)", callback_data="price_200"),
    )
    await bot.send_message(
        message.chat.id,
        "Скільки відповідей купити:",
        reply_markup=keyboard
    )

async def confirm_payment(callback_query: types.CallbackQuery):
    answers = int(callback_query.data.split("_")[1])
    buy_price = answers * 100
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="Підтвердити", callback_data=f"confirm_{buy_price}"),
        InlineKeyboardButton(text="Скасувати", callback_data="cancel"),
    )
    await bot.send_message(
        callback_query.from_user.id,
        f"Підтвердіть покупку {answers} відповідей за {buy_price} гривень:",
        reply_markup=keyboard
    )

async def cancel_payment(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "Оплату скасовано"
    )

# request for invoice
async def buy(message: types.Message):
    if config.PAYMENT_TOKEN.split(":")[1] == 'TEST':
        await bot.send_message(message.chat.id, "Test payment!")
    await bot.send_message(message.chat.id,
                           "Починаємо процес оплати"
                           "\n\nЦе ваш інвойс:", parse_mode='Markdown')
    await bot.send_invoice(
        message.chat.id,
        title="Купити",
        description=f"Оплата за {config.QUESTIONS_COUNT} запитання від бота",
        provider_token=config.PAYMENT_TOKEN,
        currency="uah",
        photo_url="https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False, # we don't need shipping fee
        prices=[types.LabeledPrice(label="Купити", amount=buy_price)],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

# pre checkout (10 seconds to answer)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, 
                                        ok=True,
                                        error_message="Упс, щось пішло не так")

# payment completion
async def successful_payment(message: types.Message):
    print("Оплата успішна:")
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")
    questions_counter = DataStorage.getQuestions(message.from_user.id) + config.QUESTIONS_COUNT
    DataStorage.updateQuestions(message.from_user.id, questions_counter)
    await bot.send_message(message.chat.id, f"Оплата по сумі {message.successful_payment.total_amount // 100} {message.successful_payment.currency} пройшла")

def register_handlers_payments(dp: Dispatcher):
    dp.register_message_handler(select_price, Text('Купити 💸'))
    dp.register_callback_query_handler(confirm_payment, lambda c: c.data and c.data.startswith('price'))
    dp.register_callback_query_handler(cancel_payment, lambda c: c.data == 'cancel')
    dp.register_callback_query_handler(buy, lambda c: c.data and c.data.startswith('confirm'))
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)