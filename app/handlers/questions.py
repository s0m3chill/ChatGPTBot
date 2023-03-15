import config
import app.util.db
import openai
from app.keyboards.inline import confirm_menu
from app.keyboards.default import general_menu, question_menu
# setup
from core import bot, DataStorage
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode


openai.api_key = config.OPENAI_TOKEN

# Define states
class ChatState(StatesGroup):
    waiting_for_message = State()
    processing_question = State()

async def start_handler(message: types.Message):
    if DataStorage.checkQuestionsLeft(message.from_user.id):
        # Ask the user to send a message to start the conversation
        await message.reply("Задавай своє питання")
        # Set the state to waiting_for_message
        # This code should be done after successful payment
        await ChatState.waiting_for_message.set()
    else:
        await message.reply("Та заплати вже, йой :(")

async def question_handler(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await ChatState.processing_question.set()
    await bot.send_message(
        message.chat.id,
        f"Чи ти підтверджуєш це питання?\n<b>{message.text}</b>",
        parse_mode='HTML',
        reply_markup=confirm_menu()
    )

# Define handler for messages
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer("Операцію скасовано", reply_markup=general_menu())

async def ask_question_no(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Confirming no")
    await state.finish()
    await call.message.answer("Поставте питання ще раз", reply_markup=question_menu())

async def ask_question_yes(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Confirming yes")
    user_data = await state.get_data()
    # Call the OpenAI API to get the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ти є живою людиною-студентом, який відповідає на запитання сесії"},
            {"role": "user", "content": user_data['question']}
        ]
    )
    # Send the response back to the user
    await call.message.answer(response.choices[0].message.content, reply_markup=question_menu())
    count = DataStorage.getQuestions(call.from_user.id) - 1
    DataStorage.updateQuestions(call.from_user.id, count)
    # Finish this state
    await state.finish()

def register_handlers_questions(dp: Dispatcher):
    dp.register_message_handler(start_handler, Text('Поставити запитання ❓'))
    dp.register_message_handler(cancel_handler, Text(equals='Скасувати ❌', ignore_case=True), state="*")
    dp.register_message_handler(question_handler, state=ChatState.waiting_for_message)
    dp.register_callback_query_handler(ask_question_no, text="confirm_no", state=ChatState.processing_question)
    dp.register_callback_query_handler(ask_question_yes, text="confirm_yes", state=ChatState.processing_question)