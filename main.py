import logging

from core import bot, dp, DataStorage
from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from aiogram import executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from app.handlers.common import register_handlers_common
from app.handlers.questions import register_handlers_questions
from app.handlers.payments import register_handlers_payments

logger = logging.getLogger(__name__)

async def on_startup(dp):
    # await DataStorage.connect()
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    register_handlers_common(dp)
    register_handlers_questions(dp)
    register_handlers_payments(dp)

async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()
    await bot.delete_webhook()

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    register_handlers_common(dp)
    register_handlers_questions(dp)
    register_handlers_payments(dp)

if __name__ == '__main__':
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )