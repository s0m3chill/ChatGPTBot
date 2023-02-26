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
    # Check if the message contains the referral parameter
    referral_user_id = referrals.decode_payload(message.get_args())
    if referral_user_id:
        referral_user_id = int(referral_user_id.split("_")[-1])
        # Check if the user is using own referral link
        if int(referral_user_id) == message.from_user.id:
            await message.reply('Ей ти, в морду дати? Своє реферал посилання не можна юзати')
        # Check if user was already referred
        elif referral_user_id in referrals.referred_users:
            await message.reply("Ви вже були зареферені") # this message is for debug purposes only, in final script, we'll remove that
        else:
            referrals.referred_users.append(referral_user_id)
            # Increment the referral counter for the user who referred someone
            if referrals.referral_count.get(int(referral_user_id)):
                referrals.referral_count[int(referral_user_id)] += 1
            else:
                referrals.referral_count[int(referral_user_id)] = 1

            # Check if the referral count has reached 3 and send congratulations message
            if referrals.referral_count.get(int(referral_user_id)) == 3:
                referrals.referral_count[int(referral_user_id)] = 0
                await bot.send_message(int(referral_user_id), "Вітаю! 3 людей долучились за допомогою твоєї рефералки!")
    await bot.send_message(message.chat.id,
                           "Привіт, я допомагаю закривати сесію, я можу продати тобі відповіді на твої запитання.\n"
                           "Напиши /buy щоб купити відповіді\n /terms для умов\n /referral_link для генерації рефералки\n /referral_status для перевірки кількості зареференних юзерів")

@dp.message_handler(commands=["terms"])
async def process_terms_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Купіть відповіді на ваші запитання, оплата дає вам 3 відповіді на запитання")
    
@dp.message_handler(commands=['referral_link'])
async def unique_link_command_handler(message: types.Message):
    user_id = referrals.encode_payload(message.from_user.id)
    referral_link = f'Тут є <a href="tg://resolve?domain=asjhdkaksjbot&start={user_id}">реферальне посилання</a>'

    # Send the referral link to the user
    await bot.send_message(
        message.chat.id,
        referral_link,
        parse_mode='HTML'
    )

@dp.message_handler(commands=['referral_status'])
async def check_status_command_handler(message: types.Message):
    user_id = message.from_user.id

    # Get the referral count for the user
    if user_id in referrals.referral_count:
        count = referrals.referral_count[user_id]
    else:
        count = 0

    # Send the referral count to the user
    await bot.send_message(
        message.chat.id,
        f"{count} людей використали твоє посилання"
    )

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
