import config
import payments
import referrals
import logging
import openai

# setup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
logging.basicConfig(level=logging.INFO)

openai.api_key = config.OPENAI_TOKEN

# init
bot = Bot(token=config.TELEGRAM_TOKEN)

storage = MemoryStorage()
# Create dispatcher object
dp = Dispatcher(bot, storage=storage)

# Define states
class ChatState(StatesGroup):
    waiting_for_message = State()

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
                await bot.send_message(int(referral_user_id), "Вітаю! Троє людей долучились через ваше посилання")
    await bot.send_message(message.chat.id,
                           "Привіт, я допомагаю закривати сесію, я можу продати тобі відповіді на твої запитання.\n"
                           "Напиши /question (тест)щоб задати питання\n/buy щоб купити відповіді\n /terms для умов\n /referral_link для генерації рефералки\n /referral_status для перевірки к-сті зареференних юзерів")

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

class ChatState(StatesGroup):
    waiting_for_message = State()

# Define handler for messages
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=ChatState.waiting_for_message)
async def cancel_handler(message: types.Message, state: FSMContext):
    # Cancel the current operation and return to the initial state
    await state.finish()
    await message.reply("Cancelled.")

@dp.message_handler(commands=['question'])
async def start_handler(message: types.Message):
    # Ask the user to send a message to start the conversation
    await message.reply("Hi there! Send me a message to get started.")
    # Set the state to waiting_for_message
    # This code should be done after successful payment
    await ChatState.waiting_for_message.set()

@dp.message_handler(state=ChatState.waiting_for_message)
async def handle_message(message: types.Message, state: FSMContext):
    # Call the OpenAI API to get the response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    # Send the response back to the user
    await message.answer(response['choices'][0]['text'])
    # Set the state to waiting_for_message
    await ChatState.waiting_for_message.set()

# run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)