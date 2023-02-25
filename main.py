import config
import payments
import logging

# setup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

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

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
