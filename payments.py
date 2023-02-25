import config
import logging

# setup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label="Купити", amount=200*100)

# commands
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Привіт, я допомагаю закривати сесію"
                           " Я можу продати тобі відповіді на твої запитання"
                           " Напиши /buy щоб купити відповіді, /terms для умов, /referral для генерації рефералки")

@dp.message_handler(commands=["terms"])
async def process_terms_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Купіть відповіді на ваші запитання, оплата дає вам 3 відповіді на запитання")
    
@dp.message_handler(commands=["referral"])
async def process_terms_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Згенерувати реферальне посилання")

# buy
@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    if config.PAYMENT_TOKEN.split(":")[1] == 'TEST':
        await bot.send_message(message.chat.id, "Test payment!")

    await bot.send_invoice(
        message.chat.id,
        title="Купити",
        description="desc",
        provider_token=config.PAYMENT_TOKEN,
        currency="uah",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )

# pre checkout (10 seconds to answer)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# payment completion
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("Оплата успішна:")
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")
    
    await bot.send_message(message.chat.id, f"Оплата по сумі {message.successful_payment.total_amount // 100} {message.successful_payment.currency} пройшла")

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
