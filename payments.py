import config
from main import *

# setup
from aiogram import types
from aiogram.types.message import ContentType

PRICE = types.LabeledPrice(label="Купити", amount=200*100)

# buy
@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    if config.PAYMENT_TOKEN.split(":")[1] == 'TEST':
        await bot.send_message(message.chat.id, "Test payment!")
    await bot.send_message(message.chat.id,
                           "Починаємо процес оплати"
                           "\n\nЦе ваш інвойс:", parse_mode='Markdown')
    await bot.send_invoice(
        message.chat.id,
        title="Купити",
        description="Оплата за 3 запитання від бота",
        provider_token=config.PAYMENT_TOKEN,
        currency="uah",
        photo_url="https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False, # we don't need shipping fee
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

# pre checkout (10 seconds to answer)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, 
                                        ok=True,
                                        error_message="Упс, щось пішло не так")

# payment completion
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("Оплата успішна:")
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")
    
    await bot.send_message(message.chat.id, f"Оплата по сумі {message.successful_payment.total_amount // 100} {message.successful_payment.currency} пройшла")