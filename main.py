import config
import referrals
import logging
import database
import keyboards as kb
import openai

# setup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher

logging.basicConfig(level=logging.INFO)

openai.api_key = config.OPENAI_TOKEN

# init
bot = Bot(token=config.TELEGRAM_TOKEN)

#initialize mongoDB
DataStorage = database.DataStore()

# Create dispatcher object
dp = Dispatcher(bot, storage=MongoStorage(uri=config.MONGODB_CONNECTION_STRING, db_name='CheatQuestionBot'))

# Define states
class ChatState(StatesGroup):
    waiting_for_message = State()

# commands
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Check if the message contains the referral parameter
    referral_user_id = referrals.decode_payload(message.get_args())
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
                           "Напиши /get <запитання> щоб поствити запитання\n/buy щоб купити відповіді\n/terms для пере\n/ref_link для генерації рефералки\n/referrals для перевірки кількості зареференних юзерів\n/questions для перевірки кількості питань\n/cancel відмінити генерацію відповіді"
                           , reply_markup=kb.greet_kb)

@dp.message_handler(Text('Інформація ℹ️'))
async def process_terms_command_button(message: types.Message):
    await process_terms_command(message)

@dp.message_handler(commands=["terms"])
async def process_terms_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Кожні 100 гривень дозволяють отримати {config.QUESTIONS_COUNT} відповіді\n"
                           f"Також для отримання 1 безкоштовоної відповіді, створи реферальне посилання та розішли його {config.REFERRALS_NEEDED} друзям. Після їхньої реєстрації ти отримаєш безкоштовну відповідь\n")

@dp.message_handler(Text('Кількість відповідей 🤓'))
async def check_questions_command_button(message: types.Message):
    await check_questions_command(message)

@dp.message_handler(commands=["questions"])
async def check_questions_command(message: types.Message):
    # Get the referral count for the user
    count = DataStorage.getQuestions(message.from_user.id)
    # Send the referral count to the user
    await bot.send_message(
        message.chat.id,
        f"Залишилося {count} питань"
    )

@dp.message_handler(Text('Рефералка 🔗'))
async def unique_link_command_button(message: types.Message):
    await unique_link_command(message)

@dp.message_handler(commands=['ref_link'])
async def unique_link_command(message: types.Message):
    user_id = referrals.encode_payload(message.from_user.id)
    referral_link = f'<a href="tg://resolve?domain=asjhdkaksjbot&start={user_id}">Клінки сюди, щоб стати рефералом</a>'

    # Send the referral link to the user
    await bot.send_message(
        message.chat.id,
        "Перешли це повідомлення друзям,аби вони стали твоїми рефералами:\n" + referral_link,
        parse_mode='HTML'
    )

@dp.message_handler(Text('Запрошені друзі 👯‍♀️'))
async def check_referrals_command_button(message: types.Message):
    await check_referrals_command(message)

@dp.message_handler(commands=['referrals'])
async def check_referrals_command(message: types.Message):
    # Get the referral count for the user
    count = DataStorage.getReferrals(message.from_user.id)
    if count == 1:
        # Send the referral count to the user
        await bot.send_message(
            message.chat.id,
            f"{count} людина використала твоє посилання"
        )
    else:
        await bot.send_message(
            message.chat.id,
            f"{count} людей використали твоє посилання"
        )

@dp.message_handler(Text('Купити 💸'))
async def buy_button(message: types.Message):
    await buy(message)

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
        description=f"Оплата за {config.QUESTIONS_COUNT} запитання від бота",
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
    questions_counter = DataStorage.getQuestions(message.from_user.id) + config.QUESTIONS_COUNT
    DataStorage.updateQuestions(message.from_user.id, questions_counter)
    await bot.send_message(message.chat.id, f"Оплата по сумі {message.successful_payment.total_amount // 100} {message.successful_payment.currency} пройшла")
    await ChatState.waiting_for_message.set()

# Define handler for messages
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=ChatState.waiting_for_message)
async def cancel_handler(message: types.Message, state: FSMContext):
    # Cancel the current operation and return to the initial state
    await state.finish()
    await message.reply("Операцію скасовано.")

@dp.message_handler(Text('Поставити запитання ❓'))
async def start_handler_button(message: types.Message):
    await start_handler(message)

@dp.message_handler(commands=['get'])
async def start_handler(message: types.Message):
    if DataStorage.checkQuestionsLeft(message.from_user.id):
        # Ask the user to send a message to start the conversation
        await message.reply("Напиши /get <запитання> щоб задати питання\n/buy щоб купити відповіді\n/terms для умов\n/ref_link для генерації рефералки\n/referrals для перевірки кількості зареференних юзерів\n/questions для перевірки кількості питань\n/cancel відмінити генерацію відповіді")
        # Set the state to waiting_for_message
        # This code should be done after successful payment
        await ChatState.waiting_for_message.set()
    else:
        await message.reply("Та заплати вже, йой :(")

@dp.message_handler(state=ChatState.waiting_for_message)
async def handle_message(message: types.Message, state: FSMContext):
    # Call the OpenAI API to get the response

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ти є живою людиною-студентом, який відповідає на запитання сесії"},
            {"role": "user", "content": message.text}
        ]
    )
    # Send the response back to the user
    await message.answer(response.choices[0].message.content)
    count = DataStorage.getQuestions(message.from_user.id) - 1
    DataStorage.updateQuestions(message.from_user.id, count)
    # Set the state to waiting_for_message
    await state.finish()

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)