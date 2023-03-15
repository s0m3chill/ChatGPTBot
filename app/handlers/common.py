import config
import app.util.referrals
import app.util.db
from app.keyboards.default import general_menu

# setup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from core import bot, DataStorage

async def cmd_start(message: types.Message):
    # Check if the message contains the referral parameter
    referral_user_id = app.util.referrals.decode_payload(message.get_args())
    if referral_user_id and referral_user_id != -1:
        referral_user_id = int(referral_user_id.split("_")[-1])
        # Check if the user is using own referral link
        if int(referral_user_id) == message.from_user.id:
            await message.reply('Ану не чітерити! Свою рефералку не можна юзати!')
        # Check if user was already referred
        elif DataStorage.checkUserInDB(message.from_user.id):
            await message.reply("Ця рефералка вже була використана.")
        else:
            #add user to the db
            DataStorage.createUser(message.from_user.id)
            # Increment the referral counter for the user who referred someone
            referrals_counter = DataStorage.getReferrals(referral_user_id) + 1
            DataStorage.updateReferrals(referral_user_id, referrals_counter)

            # Check if the referral count has reached config.QUESTIONS_COUNT and send congratulations message
            if referrals_counter == config.REFERRALS_NEEDED:
                DataStorage.updateReferrals(referral_user_id,0)
                questions_counter = DataStorage.getQuestions(referral_user_id) + 1
                DataStorage.updateQuestions(referral_user_id, questions_counter)
                await bot.send_message(int(referral_user_id), f"Вітаю! {config.REFERRALS_NEEDED} людей долучились через твоє посилання")
    await bot.send_message(message.chat.id,
                           "Привіт, я допомагаю закривати сесію та знаю відповіді на всі твої запитання)\n"
                           f"Кожні 100 гривень дозволяють отримати {config.QUESTIONS_COUNT} відповіді\n"
                           f"Також для отримання 1 безкоштовоної відповіді, створи реферальне посилання та розішли його {config.REFERRALS_NEEDED} друзям. Після їхньої реєстрації ти отримаєш безкоштовну відповідь\n"
                           , reply_markup=general_menu())

async def process_terms_handlers(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Кожні 100 гривень дозволяють отримати {config.QUESTIONS_COUNT} відповіді\n"
                           f"Також для отримання 1 безкоштовоної відповіді, створи реферальне посилання та розішли його {config.REFERRALS_NEEDED} друзям. Після їхньої реєстрації ти отримаєш безкоштовну відповідь\n")

async def check_questions_handler(message: types.Message):
    # Get the referral count for the user
    count = DataStorage.getQuestions(message.from_user.id)
    # Send the referral count to the user
    await bot.send_message(
        message.chat.id,
        f"Залишилося {count} питань"
    )

async def refferal_link_handler(message: types.Message):
    user_id = app.util.referrals.encode_payload(message.from_user.id)
    referral_link = f'<a href="tg://resolve?domain=asjhdkaksjbot&start={user_id}">Клінки сюди, щоб стати рефералом</a>'

    # Send the referral link to the user
    await bot.send_message(
        message.chat.id,
        "Перешли це повідомлення друзям,аби вони стали твоїми рефералами:\n" + referral_link,
        parse_mode='HTML'
    )

async def check_referrals_handler(message: types.Message):
    # Get the referral count for the user
    count = DataStorage.getReferrals(message.from_user.id)
    if count == 1:
        # Send the referral count to the user
        await bot.send_message(
            message.chat.id,
            f"{count} людина використала твоє посилання"
        )
    elif count == 2 or count ==3 or count == 4:
        await bot.send_message(
            message.chat.id,
            f"{count} людини використали твоє посилання"
        )
    else:
        await bot.send_message(
            message.chat.id,
            f"{count} людей використали твоє посилання"
        )

# register all handlers
def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(process_terms_handlers, Text('Інформація ℹ️'))
    dp.register_message_handler(check_questions_handler, Text('Кількість відповідей 🤓'))
    dp.register_message_handler(refferal_link_handler, Text('Рефералка 🔗'))
    dp.register_message_handler(check_referrals_handler, Text('Запрошені друзі 👯‍♀️'))