import config
from asyncio import get_event_loop
from app.util.db import DataStore
from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.TELEGRAM_TOKEN, loop=get_event_loop())
# dp = Dispatcher(bot, storage=MongoStorage(uri=config.MONGODB_CONNECTION_STRING, db_name='CheatQuestionBot'))
dp = Dispatcher(bot, storage=MemoryStorage())
#initialize mongoDB
DataStorage = DataStore()