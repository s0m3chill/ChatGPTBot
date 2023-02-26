import config
import payments
import referrals
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
    process_referrals_on_startup(message)
    await bot.send_message(message.chat.id,
                           "Привіт, я допомагаю закривати сесію, я можу продати тобі відповіді на твої запитання.\n"
                           "Напиши /buy щоб купити відповіді\n /terms для умов\n /referral_link для генерації рефералки\n /referral_status для перевірки кількості зареференних юзерів")

@dp.message_handler(commands=["terms"])
async def process_terms_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Купіть відповіді на ваші запитання, оплата дає вам 3 відповіді на запитання")
    
@dp.message_handler(commands=['referral_link'])
async def unique_link_command_handler(message: types.Message):
    process_ref_link(message)

@dp.message_handler(commands=['referral_status'])
async def check_status_command_handler(message: types.Message):
    process_ref_status(message)

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
