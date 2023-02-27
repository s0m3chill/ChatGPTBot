import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

openai.api_key = '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'
logging.basicConfig(level=logging.INFO)

# Create bot object
bot = Bot(token='5908266258:AAGjwTsYJr_mZS3UILDx8hzpiyhlHCIAquU')

storage = MemoryStorage()
# Create dispatcher object
dp = Dispatcher(bot, storage=storage)

# Define states
class ChatState(StatesGroup):
    waiting_for_message = State()

# Define handler for messages
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=ChatState.waiting_for_message)
async def cancel_handler(message: types.Message, state: FSMContext):
    # Cancel the current operation and return to the initial state
    await state.finish()
    await message.reply("Cancelled.")

@dp.message_handler(state=None)
async def start_handler(message: types.Message):
    # Ask the user to send a message to start the conversation
    await message.reply("Hi there! Send me a message to get started.")
    # Set the state to waiting_for_message
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

if __name__ == '__main__':
    # Start the long-polling process
    executor.start_polling(dp, skip_updates=True)