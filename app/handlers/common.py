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
            await message.reply('Ти не можеш використовувати власне реферальне посилання.\n'
                            f'Перешли його своїм друзям, щоб мати безкоштовні питання.')
        # Check if user was already referred
        elif DataStorage.checkUserInDB(message.from_user.id):
            await message.reply("Твій друг вже перейшов за цим посиланням.")
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
                           "Привіт, друже!👋🏻\n"
                           f"Раді представити тобі нашого бота,який вирішуватиме всі твої питання по навчанню🎓📚\n"
                           f"Наша команда розробила його саме для студентів та учнів, адже ми також ними колись були і розуміємо, як важко буває встигати все виконувати.\n\n"
                           f"Завдання, тести, реферати - все це і багато іншого наш бот зробить за вас!🤖\n\n"
                           f"Що ж, не будемо тягнути кота за хвіст і розпочнемо наше спілкування🚀\n"
                           f"Що тебе цікавить?",
                             reply_markup=general_menu())

async def process_terms_handlers(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Аби уникнути непорозумінь, ми хочемо відповісти на найбільш поширені питання:\n\n"
                            f"-Як правильно ставити запитання❓\n\n"
                            f"Запитання мусить бути якомога детальнішим і розкритим.Пам'ятай, все це пише робот, тому чим детальнішим буде опис твоєї проблеми, тим кращий результат ти отримаєш.\n"
                            f"Також,ти можеш доповнювати своє питання, уточнивши, що саме бот має додати/забрати.\n\n"
                            f"Наприклад:\n"
                            f'"Зроби текст коротшим" або "напиши це все в гумористичній манері".\n\n'
                            f"-Безкоштовні запитання😎\n\n"
                            f'Щоб отримати безкоштовне запитання, тобі потрібно натиснути на кнопку "Рефералка🔗" , після чого побачиш повідомлення,яке ти маєш переслати своїм друзям.За кожні 3 друга,які перейдуть по твоєму посиланню ти отримаєш безкоштовне питання.\n'
                            f"УВАГА!\n"
                            f"Безкоштовне питання ти отримаєш тільки тоді,коли друзі почнуть спілкування з ботом.\n"
                            f'Подивитись скільки друзів зайшли по твоєму посиланню ти можеш, натиснувши кнопку "Запрошені друзі👯‍♀️".\n'
                            f"-Оплата💵\n\n"
                            f'Ми приймаємо оплату в гривнях, на прайслист можеш подивитись натиснуваши кнопку "Купити💸".\n\n'
                            f"-Підтримка👨‍💻\n\n"
                            f"Якщо у тебе виникають проблеми,які не є зазначеними вище,ти можеш зв'язатись з нами і ми допоможемо тобі їх вирішити.Нам важливі ваші відгуки і коментарі,щоб ми могли покращувати якість бота, тим самим, роблячи його зручнішим для користування☺️\n")
async def check_questions_handler(message: types.Message):
    # Get the referral count for the user
    count = DataStorage.getQuestions(message.from_user.id)
    # Send the referral count to the user
    await bot.send_message(
        message.chat.id,
        f"Залишилося {count} питань."
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
            f"{count} людина використала твоє посилання."
        )
    elif count == 2 or count ==3 or count == 4:
        await bot.send_message(
            message.chat.id,
            f"{count} людини використали твоє посилання."
        )
    else:
        await bot.send_message(
            message.chat.id,
            f"{count} людей використали твоє посилання."
        )

# register all handlers
def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(process_terms_handlers, Text('Інформація ℹ️'))
    dp.register_message_handler(check_questions_handler, Text('Кількість відповідей 🤓'))
    dp.register_message_handler(refferal_link_handler, Text('Рефералка 🔗'))
    dp.register_message_handler(check_referrals_handler, Text('Запрошені друзі 👯‍♀️'))